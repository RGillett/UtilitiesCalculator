import datetime
import csv

class Resident:
    total = 0
    def __init__(self, name, start_date, end_date, initial):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.initial = initial
        self.total = initial

class Bill:
    def __init__(self, total, start_date, end_date):
        self.total = total
        self.start_date = start_date
        self.end_date = end_date

def show_bills(residents, bills, month):
    print(month.strftime('%B %Y') + ':')
    filtered_bills = list(filter(lambda bill: bill.end_date.year == month.year and bill.end_date.month == month.month, bills))
    
    for bill in filtered_bills:
        day_count = (bill.end_date - bill.start_date).days + 1
        for date in (bill.start_date + datetime.timedelta(n) for n in range(day_count)):
            filtered_residents = list(filter(lambda resident: resident.start_date <= date and (resident.end_date == None or date <= resident.end_date), residents))
            for resident in filtered_residents:
                resident.total += bill.total / (day_count * len(filtered_residents))

    filtered_residents = list(filter(lambda resident: resident.total > resident.initial, residents))

    total_initial = sum(resident.initial for resident in filtered_residents)
    for resident in filtered_residents:
        resident.total -= total_initial / len(filtered_residents)
        
    for resident in filtered_residents:
        print(resident.name + ': ' + "{:.2f}".format(resident.total / 1000))
        resident.total = 0 + resident.initial


##############TESTS##############
residents = []
with open('C:\\Users\\rgill\\Documents\\Code\\UtilitiesCalculator\\residents.csv', newline='') as csvfile:
    csv_residents = csv.reader(csvfile, delimiter=',', quotechar='|')
    for resident in csv_residents:
        if resident[2] == '':
            end_date = None
        else:
            end_date = datetime.datetime.strptime(resident[2], '%Y-%m-%d').date()
        if resident[3] == '':
            initial = 0
        else:
            initial = int(resident[3])*1000
        residents.append(Resident(name=resident[0], start_date=datetime.datetime.strptime(resident[1], '%Y-%m-%d').date(), end_date=end_date, initial=initial))

bills = []
with open('C:\\Users\\rgill\\Documents\\Code\\UtilitiesCalculator\\bills.csv', newline='') as csvfile:
    csv_bills = csv.reader(csvfile, delimiter=',', quotechar='|')
    for bill in csv_bills:
        bills.append(Bill(total=int(float(bill[3])*1000), start_date=datetime.datetime.strptime(bill[1], '%Y-%m-%d').date(), end_date=datetime.datetime.strptime(bill[2], '%Y-%m-%d').date()))

for year in range(2017,2021):
    for month in range(1,13):
        print('')
        show_bills(residents=residents, bills=bills, month=datetime.date(year, month, 1))