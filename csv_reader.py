import csv


class CSVReader:
    def __init__(self, filename, skip_first_row=True):
        self.filename = filename
        self.skip_first_row = skip_first_row

    def read_records(self):
        records = []
        with open(self.filename, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            if self.skip_first_row:
                next(reader)
            for row in reader:
                record = {
                    "Column1": row[0],
                    "company": row[1],
                    "line": row[2],
                    "departure_time": row[3],
                    "arrival_time": row[4],
                    "start_stop": row[5],
                    "end_stop": row[6],
                    "start_stop_lat": row[7],
                    "start_stop_lon": row[8],
                    "end_stop_lat": row[9],
                    "end_stop_lon": row[10],
                }
                records.append(record)
        return records
