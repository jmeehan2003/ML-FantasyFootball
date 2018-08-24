import bs4, requests
from bs4 import BeautifulSoup
import lxml

#pos1 = 'QB'
#yr = '2012'
#wk = '1'
#i = 0
#filename = "testfile.csv"



def scrape(yr, wk, filename):
    url = 'https://www.fantasypros.com/nfl/reports/leaders/dst.php?year=' + yr + '&start=1&end='+wk
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    r = requests.get(url, headers=headers)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    list = []

    table = soup.find_all('table')

    for row in table:
        col = row.find_all('td')
        col = [ele.text.strip() for ele in col]
        list.append([ele for ele in col if ele])
    x = 0
    j = 0
    #print(list[0][1])
    name = ""
    pos = 0
    size = len(list[0])
    #j=filename
    file = open(filename, "a")
    file.write(yr + ', ' + wk + ', ')
    for i in range(size):
        line = list[0][i] + ', '
        file.write(line)
        x += 1
        j += 1
        if x == 5:
            x = 0
            file.write('\n')
            if j != 160:
                file.write(yr + ', ' + wk + ', ')
def main():
    #arrays from which to loop
    filename = 'dscraperesults.csv'
    years = ['2012', '2013', '2014', '2015', '2016', '2017']
    for x in range(0, 6):
        print('Year: ' + str(x))
        for i in range(1, 18):
            print('Week: ' + str(i))
            scrape(years[x], str(i), filename)


#if __name__ == "__main__":
#    main()



main()