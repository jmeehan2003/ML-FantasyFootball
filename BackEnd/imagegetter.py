####################################################################################################
# Program: imagegetter.py
# Purpose: To get images url from footballdb.com Neat, right?
# Author: Eric Durboraw
####################################################################################################

import bs4, requests
from bs4 import BeautifulSoup
import lxml
import csv, psycopg2


def image_getter(lname, fname):
    #names have to be lowercase
    player_lname = lname
    player_fname = fname
    suffix = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
    x = 0
    if len(player_lname) >= 5:
        lname_sub = player_lname[:5]
    else:
        lname_sub = player_lname

    pname_url = lname_sub + player_fname[:2] + suffix[x]


    url = 'https://www.footballdb.com/players/' + player_fname + '-' + player_lname + '-' + pname_url

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
    r = requests.get(url, headers=headers)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    image = soup.find_all('img')

    if len(image) < 2:
        return 'N/A'

    #work around
    if 'cdn.footballdb.com/headshots' not in image[1]['src']:
        x += 1
        while 'cdn.footballdb.com/headshots' not in image[1]['src'] and x < 29:
            #print(x)
            pname_url = lname_sub + player_fname[:2] + suffix[x]
            url = 'https://www.footballdb.com/players/' + player_fname + '-' + player_lname + '-' + pname_url
            #print(url)
            r = requests.get(url, headers=headers)
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            image = soup.find_all('img')
            if len(image) < 2:
                return 'crap'
            #print(x)
            x += 1

    return image[1]['src']

def selector(db_name, pos):
    # Create db Connection
    conn = psycopg2.connect(database="Cepheus_db",
                            user="db_usr",
                            password="B3av3rs1!",
                            host="osucepheus.cgwruhobay1w.us-east-2.rds.amazonaws.com",
                            port="5432")

    # Create cursor with which to execute queries
    cur = conn.cursor()
    query = 'SELECT DISTINCT LOWER(TRIM(lname)), LOWER(TRIM(fname)) FROM ' + db_name

    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        #print(row)
        lname = row[0]
        fname = row[1]
        #Isaiah "Zay" Taylor needs a work around
        if fname == 'zay':
            fname = 'isaiah'
        url = image_getter(row[0], row[1])
        query = "INSERT INTO URL_XREF VALUES " + "('" + lname + "', '" + fname + "', '" + pos + "', '" + url + "')"

        cur.execute(query)

    conn.commit()

def tester(lname, fname, pos, db_name):
    # Create db Connection
    conn = psycopg2.connect(database="Cepheus_db",
                            user="db_usr",
                            password="B3av3rs1!",
                            host="osucepheus.cgwruhobay1w.us-east-2.rds.amazonaws.com",
                            port="5432")

    # Create cursor with which to execute queries
    cur = conn.cursor()
    query = 'SELECT DISTINCT LOWER(TRIM(lname)), LOWER(TRIM(fname)) FROM ' + db_name
    #print(query)
    cur.execute(query)
    rows = cur.fetchall()

    print(lname + ' ' + fname)
    url = image_getter(lname, fname)
    query = "INSERT INTO URL_XREF VALUES " + "('" + lname + "', '" + fname + "', '" + pos + "', '" + url + "')"

    cur.execute(query)

    conn.commit()

def main():

    table = ['qb_results', 'rb_results', 'wr_results', 'te_results', 'kicker_results']
    pos = ['qb', 'rb', 'wr', 'te', 'k']
    for x in range(0, 5):
        print(pos[x])
        selector(table[x], pos[x])

if __name__ == "__main__":
    main()
