#!/usr/bin/env python

# This is the implementation of Khayyam rules. year is an integer parameter.
def isLeapYearReal(year):          
    # The 2820-year cycle includes 21 128-year subcycles, and a 132-year subcycle
    cycle2820 = ((21,128),(1,132)) 
    # The 128-year subcycle includes a 29-year sub-subcycles, and three 33-year sub-subcycle
    cycle128  = ((1,29),(3,33))    
    cycle132  = ((1,29),(2,33),(1,37))
    cycle29   = ((1,5),(6,4))
    cycle33   = ((1,5),(7,4))
    cycle37   = ((1,5),(8,4))

    if year > 0:
        realYear = (year + 37) % 2820   # realYear includes zero
    elif year < 0:
        # 38 years separating the beginning of the 2820-year cycle from Hejira
        realYear = (year + 38) % 2820   
    else:
        return None                     # There is no zero year!!                     

    wi = whereIs(cycle2820, realYear)   # find what subcycle of 2820-year cycle includes the realYear
    if(wi[0] == 128):                   # if realYear is inside of 128-year subcycle 
        wi1 = whereIs(cycle128, wi[1])  # find what subcycle of 128-cycle includes the wi[1]
        if(wi1[0] == 29):               # if realYear is inside of 29-year sub-subcycle 
            wi2 = whereIs(cycle29, wi1[1])
            if wi2[1] == wi2[0] - 1:    # if wi2[1] mod wi2[0] becomes wi2[0] - 1 (wi2[0] is 4 or 5)
                return True
        elif(wi1[0] == 33):             # if realYear is inside of 33-year sub-subcycle 
            wi2 = whereIs(cycle33, wi1[1])
            if wi2[1] == wi2[0] - 1:
                return True

    elif(wi[0] == 132):                 # if realYear is inside of 132-year subcycle 
        wi1 = whereIs(cycle132, wi[1])
        if(wi1[0] == 29):
            wi2 = whereIs(cycle29, wi1[1])
            if wi2[1] == wi2[0] - 1:
                return True
        elif(wi1[0] == 33):
            wi2 = whereIs(cycle33, wi1[1])
            if wi2[1] == wi2[0] - 1:
                return True
        elif(wi1[0] == 37):
            wi2 = whereIs(cycle37, wi1[1])
            if wi2[1] == wi2[0] - 1:
                return True
    return False

def whereIs(cycle, year):            # a function to find what subcycle includes the year
    y = year
    # for example p is (21,128), which means this cycle have 21 of 128-year subcycles
    for p in cycle:                  
        if y < p[0]*p[1]:            # if y is inside one of subcycles
            # p[1] is the length of subcycle
            # y % p[1] is y mod p[1], which gives the position of y inside one of p[1]s
            return (p[1], y % p[1])  
        y -= p[0]*p[1]               # if y is not inside of p[1] subcycle prepare for next subcycle

# a function to extrapolate leap years just like isLeapYearReal(year)
def isLeapYear(year):                     
    a = 0.025                     # a and b are two parameters. which are tuned
    b = 266
    if year > 0:
        # 38 days is the difference of epoch to 2820-year cycle
        leapDays0 = ((year + 38) % 2820)*0.24219 + a  # 0.24219 ~ extra days of one year
        leapDays1 = ((year + 39) % 2820)*0.24219 + a  
    elif year < 0:
        leapDays0 = ((year + 39) % 2820)*0.24219 + a
        leapDays1 = ((year + 40) % 2820)*0.24219 + a
    else:
        # In case of using isLeapYear(year - 1) as last year. Look FixedDate function
        return True                       

    frac0 = int((leapDays0 - int(leapDays0))*1000)    # the fractions of two consecutive days
    frac1 = int((leapDays1 - int(leapDays1))*1000)

    # 242 fraction, which is the extra days of one year, can happened twice inside
    # a 266 interval so we have to check two consecutive days
    if frac0 <= b and frac1 > b : # this year is a leap year if the next year wouldn't be a leap year
        return True
    else:
        return False


# find the interval in days between FARVARDIN 1 of this year and the first one
def FixedDate(year):          
    if year > 0:
        realYear = year - 1   # realYear includes zero
    elif year < 0:
        realYear = year
    else:
        return None           # There is no zero year!!

    days = 1029983 * int( (realYear + 38) / 2820 ) # 1029983 is the total days of one 2820-year cycle
    cycle = (realYear + 38) % 2820                 # cycle is (realYear + 38) mod 2820
    days += int((cycle - 38) * 365.24219) + 1
    if cycle - 38 < 0:
        days -= 1
    extra = cycle * 0.24219                         # 0.24219 ~ extra days of one year
    frac = int((extra - int(extra))*1000)           # frac is the fraction of extra days
    if isLeapYear(year - 1) and frac <= 202:        # 202 is a tuned parameter
        days += 1

    return days

def test():
    days = 1                                         # The first day of calendar, FARVARDIN 1, 1
    for year in range(1,2850):
        # check if the estimated function is the same as the real one
        if isLeapYear(year) != isLeapYearReal(year): 
            print "wrong!!"

        if FixedDate(year) != days:
            print "wrong!!"

        if isLeapYear(year):                         # add 366 days for leap years
            days += 366
        else:
            days += 365

    days = 1                                         # The first day of calendar, FARVARDIN 1, 1
    for year in range(-1,-2850,-1):                  # do the same for negative years
        if isLeapYear(year) != isLeapYearReal(year):
            print "wrong!!"

        if isLeapYear(year):
            days -= 366
        else:
            days -= 365

        if FixedDate(year) != days:
            print "wrong!!"

test()
