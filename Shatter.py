#!/usr/bin/env python
from os import system
from PIL import Image
import numpy as np
import os, sys, codecs, time, random
 
# Thanks to Xylozi for the flag generation code
 
if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' eu4dir')
    sys.exit()
 
eu4dir = sys.argv[1]
if eu4dir[-1] != '/':
    eu4dir = eu4dir + '/'
 
colordiversion = 20
 
system('rm -rf provincecountries')
 
time.sleep(0.5)
 
system('mkdir provincecountries')
system('mkdir provincecountries/history')
system('mkdir provincecountries/gfx')
system('mkdir provincecountries/common')
system('mkdir provincecountries/localisation')
 
provincehistoryoutpath = 'provincecountries/history/provinces/'
system('mkdir ' + provincehistoryoutpath)
 
countryhistoryoutpath = 'provincecountries/history/countries/'
system('mkdir ' + countryhistoryoutpath)
 
countrydataoutpath = 'provincecountries/common/countries/'
system('mkdir ' + countrydataoutpath)
 
countrytagsoutpath = 'provincecountries/common/country_tags/'
system('mkdir ' + countrytagsoutpath)
 
flagpath = 'provincecountries/gfx/flags/'
system('mkdir ' + flagpath)
 
print('Please resave "Europa Universalis IV/gfx/interface/client_state_symbols_large.dds" in this directory with "BC3 / DXT5" compression.')
 
flagsize = 128
symbolsize = 64
flagpatternpath = [eu4dir + p for p in\
    ['gfx/custom_flags/pattern.tga', 'gfx/custom_flags/pattern2.tga']]
flagsymbolpath = ['client_state_symbols_large.dds']
 
patternImage = [Image.open(p) for p in flagpatternpath]
symbolImage = [Image.open(p) for p in flagsymbolpath]
 
flagPatternList = []
flagSymbolList = []
 
niceflagcolors = [  (0xff, 0xff, 0xff), (0x00, 0x62, 0x33), (0xd2, 0x10, 0x34),\
                    (0x00, 0x00, 0x00), (0xf9, 0xd6, 0x16), (0x00, 0x87, 0x51),\
                    (0x6a, 0xb2, 0xe7), (0x00, 0x0f, 0xff), (0x00, 0x6b, 0x3f),\
                    (0xa3, 0x66, 0x29), (0x00, 0x96, 0x6e), (0x11, 0x45, 0x7e),\
                    (0xd0, 0xd0, 0xd0), (0xfd, 0xb9, 0x13), (0xff, 0xa7, 0x1a)]
 
for patternFile in patternImage:
    for x in range(patternFile.size[0]//flagsize):
        for y in range(patternFile.size[1]//flagsize):
            flagPatternList.append(patternFile.crop((x * flagsize, y * flagsize, (x+1) * flagsize, (y+1)*flagsize)))
 
for symbolFile in symbolImage:
    for x in range(symbolFile.size[0]//symbolsize):
        for y in range(symbolFile.size[1]//symbolsize):
            flagSymbolList.append(symbolFile.crop((x * symbolsize, y * symbolsize, (x+1) * symbolsize, (y+1)*symbolsize)))
 
system('ls "' + eu4dir + 'history/provinces" -v > provinces.txt')
provincelist = open('provinces.txt', 'r').readlines()
system('rm provinces.txt')
 
system('ls "' + eu4dir + 'history/countries" -v > countries.txt')
countrylist = open('countries.txt', 'r').readlines()
system('rm countries.txt')
 
langfile = open('provincecountries/localisation/countries_l_english.yml', 'w', encoding='utf-8', errors='ignore')
oldcountrylangfile = codecs.open(eu4dir + 'localisation/countries_l_english.yml', encoding='utf-8', errors='ignore').readlines()
# Okay we even need files like manchu_l_english.yml so let's just take all the _l_english.yml files and concat them
megalangfilename = 'megalangfile.yml'
system('cat ' + eu4dir + 'localisation/*_l_english.yml > ./' + megalangfilename)
megalangfile = codecs.open(megalangfilename, encoding='utf-8', errors='ignore').readlines()

#oldprovincenamefile = codecs.open(eu4dir + 'localisation/prov_names_l_english.yml', encoding='utf-8', errors='ignore').readlines()
#oldprovinceadjfile = codecs.open(eu4dir + 'localisation/prov_names_adj_l_english.yml', encoding='utf-8', errors='ignore').readlines()
countrytagoutfile = open(countrytagsoutpath + 'shatteredcountries.txt', 'w')
oldtagfile = codecs.open(eu4dir + 'common/country_tags/00_countries.txt', encoding='utf-8', errors='ignore').readlines()
 
def splitints(line):
    l = []
    for w in line.replace('{', ' ').replace('}', ' ').split(' '):
        if w.isdigit():
            l.append(w)
    return l
 
def terminate():
    system('rm currentcountry.txt')
    countrytagoutfile.close()
    langfile.close()
    sys.exit()
 
def tag(i):
    i = int(i) - 1
    s = ''
    s += chr(ord('A') + (i // (ord('Z') - ord('A') + 1)**2))
    i = i % (ord('Z') - ord('A') + 1)**2
    s += chr(ord('A') + (i // (ord('Z') - ord('A') + 1)))
    i = i % (ord('Z') - ord('A') + 1)
    s += chr(ord('A') + i)
    return s
 
def istagtaken(s):
    for line in countrylist:
        if line.startswith(s):
            return True
    return False
 
def qtwrd(s):
    ans = ''
    going = 0
    for w in s.replace('\t', ' ').split(' '):
        if going == 1:
            ans += ' ' + w
            if w[-1] == '\"':
                going = 0
        if len(w) > 0 and w[0] == '\"':
            ans = w
            if w[-1] != '\"':
                going = 1
    return ans
 
def parseprovincename(provinceid):
    provinceid = provinceid.replace('-', ' ').split(' ')[0]
    for line in megalangfile:
        line = line.replace('\t', ' ')
        if line.startswith(' PROV' + provinceid + ':'):
            if line[-1] == '\n':
                line = line[:-1]
            if line[-1] == '\r':
                line = line[:-1]
            return qtwrd(line)
 
def parseprovinceadjective(provinceid):
    provinceid = provinceid.replace('-', ' ').split(' ')[0]
    for line in megalangfile:
        line = line.replace('\t', ' ')
        if line.startswith(' PROV_ADJ' + provinceid + ':'):
            if line[-1] == '\n':
                line = line[:-1]
            if line[-1] == '\r':
                line = line[:-1]
            return qtwrd(line)
 
def findowner(s):
    ind = s.find('owner = ')
    return s[ind + 8:ind + 11]
 
nextid = 1
 
#langfile.write('l_english:\r\n')
for line in oldcountrylangfile:
    langfile.write(line)
 
for provincefilename in provincelist:
    provincefilename = provincefilename[:-1]
    provinceid = provincefilename.replace('-', ' ').split(' ')[0]
    #print('Province ID: ' + provinceid)
    provincename = provincefilename.replace('-', ' ').split(' ')[-1][:-4]
 
    provincehistoryfile = codecs.open(eu4dir + 'history/provinces/' + provincefilename, encoding='utf-8', errors='ignore').readlines()
    print('ID: ' + provinceid + ', path: ' + provincefilename)
    oldcountrytag = ''
    going = 0
    for line in provincehistoryfile:
        line = line.replace('\t', ' ')
 
        fem = line.find('owner = ')
 
        if line.startswith('1'):
 
            year = int(line.split('.')[0])
            month = int(line.split('.')[1])
            day = int(line.split('.')[2].replace('=', ' ').split(' ')[0])
            if day + month * 40 + year * 40*15 > 11 + 11*40 + 1444 * 40*15:
                break
 
        if fem != -1:
            oldcountrytag = findowner(line)
 
 
    provincehistoryoutfile = open(provincehistoryoutpath + provincefilename, 'w')
 
    if oldcountrytag != '':
        # Collect some data about the province
        culture = ''
        religion = ''
 
        for line in provincehistoryfile:
            line = line.replace('\t', ' ')
            if line.startswith('culture'):
                culture = line.split(' ')[2]
            if line.startswith('religion'):
                religion = line.split(' ')[2]
 
        # Collect data about the past owner
        government = ''
        mercantilism = ''
        primary_culture = ''
        technology_group = ''
        unit_type = ''
        capital = ''
 
        # Let's read the country data very hackishly
        system('cat \"' + eu4dir + 'history/countries\"/' + oldcountrytag + '* > currentcountry.txt')
        oldcountryfile = codecs.open('currentcountry.txt', encoding='utf-8', errors='ignore').readlines()
 
        # And now parse it
        for line in oldcountryfile:
            line = line.replace('\t', ' ')
            if line.startswith('government '):
                government = line[:-1].split(' ')[2]
            if line.startswith('mercantilism'):
                mercantilism = line[:-1].split(' ')[2]
            if line.startswith('primary_culture'):
                primary_culture = line[:-1].split(' ')[2]
            if line.startswith('technology_group'):
                technology_group = line[:-1].split(' ')[2]
            if line.startswith('unit_type'):
                unit_type = line[:-1].split(' ')[2]
            if line.startswith('capital'):
                capital = line[:-1].split(' ')[2]
 
        if len(government) < 3:
            print('Reading government failed!')
            terminate()
 
        if capital == provinceid:
            #If this province is the capital, don't modify it.
            for ln in provincehistoryfile:
                provincehistoryoutfile.write(ln)
            continue
 
        countrytag = tag(nextid)
        nextid += 1
        while istagtaken(countrytag) or countrytag in ['AGE', 'AUX', 'CAV', 'CON']:
            countrytag = tag(nextid)
            nextid += 1
 
        countryoutfilepath = countrytag + ' - ' + ' '.join(provincefilename.replace('-', ' ').split()[1:])
 
        countryname = parseprovincename(provincefilename)
        # Create a new country for the province if it was owned and not the capital
        countrytagoutfile.write(countrytag + ' = "countries/' + countryoutfilepath + '"\r\n')
 
        # And add info to the province file!
        provincehistoryoutfile.write('owner = ' + countrytag + '\r\n')
        provincehistoryoutfile.write('controller = ' + countrytag + '\r\n')
        provincehistoryoutfile.write('add_core = ' + countrytag + '\r\n')
 
        # And let's write the country file!
        countryhistoryoutfile = open(countryhistoryoutpath + countryoutfilepath, 'w')
 
        countryhistoryoutfile.write('government = ' + government + '\r\n')
        countryhistoryoutfile.write('government_rank = 1\r\n')
 
        # Write mercantilism only if we found a value for it
        if mercantilism != '':
            countryhistoryoutfile.write('mercantilism = ' + mercantilism + '\r\n')
 
        countryhistoryoutfile.write('technology_group = ' + technology_group + '\r\n')
        countryhistoryoutfile.write('religion = ' + religion + '\r\n')
        countryhistoryoutfile.write('primary_culture = ' + culture + '\r\n')
        countryhistoryoutfile.write('capital = ' + provinceid + '\r\n')
 
        countryhistoryoutfile.close()
 
        oldcountryfilename = ''
        # Hack time again!
        for line in oldtagfile:
            line = line.replace('\t', ' ')
 
            if line.startswith(oldcountrytag):
                oldcountryfilename = qtwrd(line)
                if oldcountryfilename[-1] == '\n':
                    oldcountryfilename = oldcountryfilename[:-1]
                if oldcountryfilename[-1] == '\r':
                    oldcountryfilename = oldcountryfilename[:-1]
 
        system('cat "' + eu4dir + 'common/' + oldcountryfilename[1:] + ' > currentcountry.txt')
        countrydataoldfile = codecs.open('currentcountry.txt', encoding='utf-8', errors='ignore').readlines()
        countrydataoutfile = open(countrydataoutpath + countryoutfilepath, 'w')
 
        graphical_culture = ''
        colorr = 0
        colorb = 0
        colorg = 0
 
        keepgoing = 0
 
        for line in countrydataoldfile:
            line = line.replace('\t', ' ')
 
            if keepgoing == 1:
                countrydataoutfile.write(line)
                if line.startswith('}'):
                    keepgoing = 0
 
                continue
 
            if line.startswith('graphical_culture'):
                countrydataoutfile.write(line)
 
            if line.startswith('color'):
                colors = splitints(line)
                for i, _ in enumerate(colors):
                    colors[i] = int(colors[i]) + random.randint(-colordiversion, colordiversion)
                    if colors[i] < 0:
                        colors[i] = 0
                    if colors[i] > 255:
                        colors[i] = 255
 
                colorr, colorb, colorg = colors
 
                countrydataoutfile.write('color = { ' + str(colorr) + ' ' + str(colorb) + ' ' + str(colorg) + ' }\r\n')
 
            if line.startswith('historical_idea_groups'):
                countrydataoutfile.write(line)
                keepgoing = 1
 
            if line.startswith('historical_units'):
                countrydataoutfile.write(line)
                keepgoing = 1
 
            if line.startswith('monarch_names'):
                countrydataoutfile.write(line)
                keepgoing = 1
 
            if line.startswith('leader_names'):
                countrydataoutfile.write(line)
                keepgoing = 1
 
            if line.startswith('ship_names'):
                countrydataoutfile.write(line)
                keepgoing = 1
 
            if line.startswith('army_names'):
                countrydataoutfile.write(line)
                keepgoing = 1
 
            if line.startswith('fleet_names'):
                countrydataoutfile.write(line)
                keepgoing = 1
 
        countrydataoutfile.close()
 
        adjective = parseprovinceadjective(provinceid)
 
        langfile.write(' ' + countrytag + ':0 ' + countryname + '\r\n')
        langfile.write(' ' + countrytag + '_ADJ:0 ' + adjective + '\r\n')
 
        # Make flag
 
        flag = Image.new('RGB', (flagsize, flagsize))
        flag.paste(random.choice(flagPatternList))
 
        flag = flag.convert('RGBA')
 
        flagImageData = np.array(flag)
        red, green, blue, alpha = flagImageData.T
 
        red_areas   = (red != 0)
        green_areas = (green != 0)
        blue_areas  = (blue != 0)
 
        flagImageData[..., :-1][red_areas.T]   = random.choice(niceflagcolors)
        flagImageData[..., :-1][green_areas.T] = random.choice(niceflagcolors)
        flagImageData[..., :-1][blue_areas.T]  = random.choice(niceflagcolors)
 
        flag = Image.fromarray(flagImageData)
 
        symbol = random.choice(flagSymbolList)
        flag.paste(symbol, ((flagsize - symbolsize)//2, (flagsize - symbolsize)//2), symbol)
 
        flag.save(flagpath + countrytag + '.tga')
 
        ## Copy flag
        #system('cp ../gfx/flags/' + oldcountrytag + '.tga ' + flagpath + countrytag + '.tga')
 
    for line in provincehistoryfile:
        line = line.replace('\t', ' ')
 
        # if line.startswith('1'):
        #   year = int(line.split('.')[0])
        #   month = int(line.split('.')[1])
        #   day = int(line.split('.')[2].replace('=', ' ').split(' ')[0])
        #   if day + month * 31 + year * 31*12 > 11 + 11 * 31 + 1444 * 31*12:
        #       break
 
        if oldcountrytag == '':
            provincehistoryoutfile.write(line)
        else:
            provincehistoryoutfile.write(line.replace(oldcountrytag, countrytag))
 
    provincehistoryoutfile.close()
 
print("All files were generated. Have a great day!")
 
terminate()
