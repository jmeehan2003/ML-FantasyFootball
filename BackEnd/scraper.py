import bs4, requests
from bs4 import BeautifulSoup
import lxml

#pos1 = 'QB'
#yr = '2012'
#wk = '1'
#i = 0
#filename = "testfile.csv"



def nameHandler(name, file):
    if name.count('.') == 1:  # not a name like C.J. or T.J.
        pos = name.find('.')
        name = name[:pos - 1]
        name = name.split(" ")
        fname = name[0]
        lname = name[1]
        file.write(lname + ", " + fname + ", ")
    else:
        pos = name.find('0')
        name = name[:pos - 7]
        name = name.split(" ")
        fname = name[0]
        lname = name[1]
        if fname == 'T.J.' and lname[0] == 'Y' and lname[1] == 'a':
            fname = 'TJ'
            lname = 'Yates'
        elif fname == 'T.J.' and lname[0] == 'Y' and lname[1] == 'e':
            fname = 'TJ'
            lname = 'Yeldon'
        elif fname == 'T.J.' and lname[0] == 'G':
            fname = 'TJ'
            lname = 'Graham'
        elif fname == 'E.J.' and lname[0]=='M':
            fname = 'EJ'
            lname = 'Manuel'
        elif fname == 'E.J.' and lname[0]=='B':
            fname = 'EJ'
            lname = 'Bibbs'
        elif fname == 'A.J.' and lname[0]=='G':
            fname = 'AJ'
            lname = 'Green'
        elif fname == 'A.J.' and lname[0]=='J':
            fname = 'AJ'
            lname = 'Jenkins'
        elif fname == 'A.J.' and lname[0]=='D':
            fname = 'AJ'
            lname = 'Derby'
        elif fname == 'A.J.' and lname[0] == 'M':
            fname = 'AJ'
            lname = 'McCaron'
        elif lname[0] == 'B' and fname == 'C.J.':
            lname = 'Beathard'
            fname = 'CJ'
        elif lname[0] == 'S' and fname == 'C.J.':
            lname = 'Spiller'
            fname = 'CJ'
        elif lname[0] == 'A' and fname == 'C.J.':
            lname = 'Anderson'
            fname = 'CJ'
        elif lname[0] == 'P' and fname == 'C.J.':
            lname = 'Prosise'
            fname = 'CJ'
        elif lname[0] == 'H' and fname == 'C.J.':
            lname = 'Ham'
            fname = 'CJ'
        elif lname[0] == 'F' and fname == 'C.J.':
            lname = 'Fiedorowicz'
            fname = 'CJ'
        elif lname[0] == 'U' and fname == 'C.J.':
            lname = 'Uzomah'
            fname = 'CJ'
        elif lname=='War':
            lname = 'Ware'
            fname = 'DJ'
        elif lname=='WilliamsD.':
            lname = 'Williams'
            fname = 'DJ'
        elif lname=='TialaveaD.':
            lname = 'Tialavea'
            fname = 'DJ'
        elif lname=='FosterD':
            lname = 'Foster'
            fname = 'DJ'
        elif fname == ' T.Y.' or lname == 'HiltonT':
            lname = 'Hilton'
            fname = 'TY'
        elif fname == 'J.J.':
            lname = 'Nelson'
            fname = 'JJ'
        elif fname == 'J.D.':
            lname = 'McKissic'
            fname = 'JD'
        elif fname == 'O.J.':
            lname = 'Howard'
            fname = 'OJ'
        elif fname == 'B.J.':
            lname = 'Daniels'
            fname = 'OJ'
        file.write(lname + ", " + fname + ", ")

def defNameHandler(name, file):
    mlength = len(name)
    mlength = mlength - 1
    while name[mlength].isupper():
        mlength = mlength - 1
    mlength = mlength + 1 #I feel like I'm using a bomb to kill a mouse...
    three_let = name[mlength:]
    long_name = name[:mlength]
    file.write(long_name + ", " + three_let + ", ")

def scrape(pos1, yr, wk, filename):
    url = 'http://www.footballdb.com/fantasy-football/index.html?pos=' + pos1 + '&yr=' + yr + '&wk=' + wk + '&rules=1'
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
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
    name = ""
    pos = 0
    size = len(list[0])
    j=0
    file = open(filename, "a")

#tracking new rows

    if pos1 == 'K':
        #file.write("League_Yr, Wk, lname, fname, Team1, Team2, Pts, XPA, XPM, FGA, FGM, GT50\n")
        stop = 8
    elif pos1 == 'DST':
        #file.write("League_Yr, Wk, name_sht, home, opp, Pts, Sack, int, Saf, FR, Blk, Td, PA, PassYds, RushYds, Totyds\n")
        stop = 13
    else:
        #file.write("League_Yr, wk, lname, fname, Team1, Team2, Pts, PAtt, PCmp, PYds, PTD, PInt, P2Pt, RuAtt, RuYds, RuTD, Ru2pts, ReRec, ReYds, ReTD, Re2pt, FuFL, FuTD")
        stop = 19

    for i in range(size):
        if j == 0:
            file.write(yr + ", " + wk + ", ")
            name = list[0][i]
            if pos1 == 'DST':
                defNameHandler(name, file)
            else:
                nameHandler(name, file)
            j += 1
        elif j == 1: #split the match up field into two team fields
            match = list[0][i]
            if match[0] == 'v':
                home = 'y'
            else:
                home = 'n'
            if pos1 == 'DST':
                mlength = len(list[0][i])
                mlength = mlength - 1
                while list[0][i][mlength].isupper():
                    mlength = mlength - 1
                three_let = match[mlength:]
                file.write(home + ", " + three_let + ", ")
            else:
                pos = match.find('@')
                pteam = match[:pos]
                oteam = match[pos + 1:]
                file.write(pteam + ", " + oteam + ", ")
            j += 1
        else:
            writevar = list[0][i] + ", "
            file.write(writevar)
            j += 1
        if j == stop:
            file.write("\n")
            j = 0

    file.close()

def main():
    #arrays from which to loop
    pos = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
    yr1 = ['2012', '2013', '2014', '2015', '2016', '2017']
    fnames = ["QB Results.csv", "RB Results.csv", "WR Results.csv", "TE Results.csv", "K Results.csv",
              "DST Results.csv"]
    weeks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
    #scrape('K', '2012', '1', "DST Results.csv") -- Test
    postracker = ['QB', 0]
    for x in range(0,6): #for position and file names
        pos1 = pos[x]
        print(pos1)
        filename = fnames[x]
        file = open(filename, "a")
        #adding a header
        if pos1 != postracker[0]:
            postracker[0] = pos1
            postracker[1] = 0
        if postracker[1] == 0:
            if pos1 == 'K':
                file.write("League_Yr, Wk, lname, fname, Team1, Team2, Pts, XPA, XPM, FGA, FGM, GT50\n")
            elif pos1 == 'DST':
                file.write("League_Yr, Wk, name_sht, home, opp, Pts, Sack, int, Saf, FR, Blk, Td, PA, PassYds, RushYds, Totyds\n")
            else:
                file.write("League_Yr, wk, lname, fname, Team1, Team2, Pts, PAtt, PCmp, PYds, PTD, PInt, P2Pt, RuAtt, RuYds, RuTD, Ru2pts, ReRec, ReYds, ReTD, Re2pt, FuFL, FuTD\n")
            file.close()
            postracker[1] = 1
        print(filename)
        for years in yr1:
            yr = years
            print(yr)
            for week in weeks:
                wk = week
                print(wk)
                scrape(pos1, yr, wk, filename)

if __name__ == "__main__":
    main()



#main()