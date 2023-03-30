from db_table import db_table
import sys

def main(col, val):
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

# find all matching sessions
    if(col=="speaker"):
        val = "%" + val + "%"
    output = agenda.select(where = {col: val})

# find all matching subsessions
    for row in output:
        suboutput = subsessions.select(where = {"date": row['date'], "time_start": row['time_start'], "title": row['title']})
        for subrow in suboutput:
            output = output + agenda.select(where = {"date": subrow['sub_date'], "time_start": subrow['sub_time_start'], "title": subrow['sub_title']})

# print answer
    for row in output:
        print(str(row) + "\n\n")

    agenda.close()
    subsessions.close()



if __name__ == "__main__":
# column string
    col = sys.argv[1]
# value string
    val = sys.argv[2:]
    val = " ".join(val)
    main(col, val)