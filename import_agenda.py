from db_table import db_table
import xlrd
import sys
import re

# add sql escape chars to str
def escape_string(dirty_str):
    clean_str = re.sub("\'", "\'\'", dirty_str)
    return(clean_str)

def main(fn):
# initialise agenda table
    name = "agenda"
    schema = {"date": "text not null", "time_start": "text not null", "time_end": "text not null", "title": "text not null", "location": "text", "description": "text", "speaker": "text"}
    constraints = ", primary key (date, time_start, title)"
    agenda = db_table(name, schema, constraints)

# initialise subsessions table
    name = "subsessions"
    schema = {"date": "text not null", "time_start": "text not null", "title": "text not null", "sub_date": "text not null", "sub_time_start": "text not null", "sub_title": "text not null", }
    constraints = ", primary key (sub_date, sub_time_start, sub_title), foreign key (date, time_start, title) references agenda(date, time_start, title)"
    subsessions = db_table(name, schema, constraints)

# access data from given file
    data = xlrd.open_workbook(fn).sheet_by_index(0)

# save primary key if not a subsession to be used in case subessions exist
    super_date = ""
    super_time_start = ""
    super_title = ""
# from row 16 to end, insert all record in the tables
    for rx in range(15, data.nrows):
    # insert record into agenda
        a_record = {}
        a_record.update({"date": data.cell_value(rx, 0)})
        a_record.update({"time_start": data.cell_value(rx, 1)})
        a_record.update({"time_end": data.cell_value(rx, 2)})
        a_record.update({"title": escape_string(data.cell_value(rx, 4))})
        a_record.update({"location": escape_string(data.cell_value(rx, 5))})
        a_record.update({"description": escape_string(data.cell_value(rx, 6))})
        a_record.update({"speaker": escape_string(data.cell_value(rx, 7))})
        agenda.insert(a_record)

    # session column
        type = data.cell_value(rx, 3)
        if(type==None):
            print("Error in database: Session column in row %d" %(rx))
            agenda.close()
            subsessions.close()
            exit()

    # if session, save primary key
        if(type=="Session"):
            super_date = a_record["date"]
            super_time_start = a_record["time_start"]
            super_title = a_record["title"]
    # else add to subsession table
        elif(type=="Sub"):
            s_record = {}
            s_record.update({"date": super_date})
            s_record.update({"time_start": super_time_start})
            s_record.update({"title": super_title})
            s_record.update({"sub_date": a_record["date"]})
            s_record.update({"sub_time_start": a_record["time_start"]})
            s_record.update({"sub_title": a_record["title"]})
            subsessions.insert(s_record)
        else:
            print("Error in database: Session column in row %d" %(rx))
            agenda.close()
            subsessions.close()
            exit()
    
    agenda.close()
    subsessions.close()
        

        

if __name__ == "__main__":
# .xls db file name
    fn = sys.argv[1]
    main(fn)
