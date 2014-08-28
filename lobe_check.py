#!/usr/bin/python

import psycopg2
import sys
import pprint

def calculation(cursor,switch):
    cursor.execute("SELECT st_area(ST_ConvexHull(ST_Collect(lobe))) FROM public.pde20121212 WHERE msc='%s'" %  switch)
    records = cursor.fetchone()

    cursor.execute("SELECT st_area( st_union) FROM (SELECT ST_union(lobe) FROM public.pde20121212 WHERE msc ='%s')a" % switch)
    filter = cursor.fetchone()
    
    try:
        covered_area = float(filter[0])
        total_area = float(records[0])
    except:
        print "Avoiding switch %s / probably decomossioned" % switch
        return switch,0



    # calculation

    p_cover = (covered_area / total_area) * 100
    #pprint.pprint (filter)
    #pprint.pprint (records)
    return switch,p_cover




def main():
    conn_string = "host='10.255.0.218' dbname='mega' user='mega' password='mega!'"
    #conn_string = "host='10.255.3.20' dbname='mega' user='mega' password='mega!'"
    #Print the connection string we will use to connect
    #print "Connecting to database\n =>%s" % (conn_string)

    #Get a connection, if a connection can not be made an exception will be raised

    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object , you can use this curson to perform queries
    cursor = conn.cursor()
    #print "Connected!\n"

    #################################### Getting the list of Switches ################################################
    sw_list=set()

    #cursor.execute("SELECT msc  FROM public.pde20121212")
    cursor.execute("SELECT msc  FROM public.lcib20131016")
    all_sw = cursor.fetchall()
    for i,switch in enumerate(all_sw):
        sw_list.add(switch[0])

    final = dict()

    # Print all set elements
    for i,msc in enumerate(sw_list):
            #print i,msc
            switch,parea=calculation(cursor,msc)
            #print "Switch %s  , Percentage= %f" % (msc,parea)
            final[switch]=parea

    ##################################### Finding Bad switches       ##################################################
    bad_list=dict()
    for switch,val in final.items():
        if val <= 60.0:
            bad_list[switch] = val


    # print bad list

    for sw,val in bad_list.items():
        print "%s\t%f" % (sw,val)


if __name__=='__main__':
    main()
