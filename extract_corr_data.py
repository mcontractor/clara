from html2text import elements
import xlrd
import os
from xlwt import Workbook

path = "/home/mc1927/clara/batch_tests/1554A/"

wb = Workbook()
sheet1 = wb.add_sheet('test 1')
sheet1.write(0,0, 'File')
sheet1.write(0,1, 'Repairs')
sheet1.write(0,2, 'Correct Repairs')
sheet1.write(0,3, 'Partial Repairs')
sheet1.write(0,4, 'Structure Mismatchs 0')
sheet1.write(0,5, 'Structure Mismatchs 1')
sheet1.write(0,6, 'Structure Mismatchs 2')
sheet1.write(0,7, 'Structure Mismatchs 3')
sheet1.write(0,8, 'Max Locs Removed')
sheet1.write(0,9, 'Min Locs Removed')
sheet1.write(0,10, 'Max Locs Added')
sheet1.write(0,11, 'Min Locs Added')
sheet1.write(0,12, 'Parse Errors')
sheet1.write(0,13, 'Max Cost 0')
sheet1.write(0,14, 'Min Cost 0')
sheet1.write(0,15, 'Max Cost 1')
sheet1.write(0,16, 'Min Cost 1')
sheet1.write(0,17, 'Max Cost 2')
sheet1.write(0,18, 'Min Cost 2')
sheet1.write(0,19, 'Max Cost 3')
sheet1.write(0,20, 'Min Cost 3')
sheet1.write(0,21, 'Timeouts')
sheet1.write(0,22, 'Total runs')
sheet1.write(0,23, 'Corr Rep 0')
sheet1.write(0,24, 'Corr Rep 1')
sheet1.write(0,25, 'Corr Rep 2')
sheet1.write(0,26, 'Corr Rep 3')
sheet1.write(0,27, 'wrong test case')
i = 1
# probs = ['1551A.xls', '1560B.xls', '1554A.xls', '276A.xls', '716A.xls', '1467A.xls', '977C.xls']
AllCorrectProgs = {}
Progs = {}
correct = [
"134421801",
"137593443",
"139037081",
"136136048",
"141824639",
"141364911",
"142772825",
"133904059",
"136299250",
"137791508",
"146510580",
"143543133",
"141611511",
"134507857",
"140296382",
"138699322",
"142115909",
"134490571",
"144809421",
"142616589",
"134365073",
"146280589",
"142944908",
"137714968",
"133380987",
"133259378",
"134779401",
"142038218",
"145962497",
"141735863",
"136304768",
"135896521",
"133124953",
"137197832",
"136176581",
"136221644",
"142116020",
"145146319",
"146495296",
"139981511",
"140372751",
"143138890",
"134364994",
"142243406",
"133090666",
"132701466",
"132628055",
"131116158",
"130978389",
"130794595"
]
for f in correct:
    AllCorrectProgs[f] = {
'reps' : 0,
'correct_reps' : 0,
'mismatch0' : 0,
'mismatch1' : 0,
'mismatch2' : 0,
'mismatch3' : 0,
'parse_err' : 0,
'partial_reps' : 0,
'runs' : 0,
'timeouts' : 0,
'min_cost' : 99999999,
'max_cost' : 0,
'min_cost1' : 99999999,
'max_cost1' : 0,
'min_cost2' : 99999999,
'max_cost2' : 0,
'min_cost3' : 99999999,
'max_cost3' : 0,
'min_loc_added' : 99999999,
'max_loc_added' : 0,
'min_loc_rem' : 99999999,
'max_loc_rem' : 0,
'corr_rep0' : 0,
'corr_rep1' : 0,
'corr_rep2' : 0,
'corr_rep3' : 0,
'testcase' : False,
}
    Progs[f] = set()

# for probname in probs:
for probname in os.listdir(path):
    if '_3' not in probname:
        continue

    prob_wb = xlrd.open_workbook(path+probname)
    prob_sheet = prob_wb.sheet_by_index(0)

    for j in range(1,prob_sheet.nrows):
        name = prob_sheet.cell_value(j,1)
        name_c = str(prob_sheet.cell_value(j,0))

        AllCorrectProgs[name_c]['runs'] += 1
        if prob_sheet.cell_value(j, 7) != 'Yes' :
            AllCorrectProgs[name_c]['testcase'] = True
            continue
        # original rep
        if (prob_sheet.cell_value(j,11) == 0):
            if prob_sheet.cell_value(j, 3) == 'True':
                AllCorrectProgs[name_c]['mismatch0'] += 1
            else:
                if (prob_sheet.cell_value(j, 4) == 'Yes'):
                    Progs[name_c].add(name)
                    AllCorrectProgs[name_c]['corr_rep0']+=1
                    AllCorrectProgs[name_c]['min_cost'] = min(AllCorrectProgs[name_c]['min_cost'], float(prob_sheet.cell_value(j, 12)))
                    AllCorrectProgs[name_c]['max_cost'] = max(AllCorrectProgs[name_c]['max_cost'], float(prob_sheet.cell_value(j, 12)))
        
        # edges + labels + corr prog edges
        elif (prob_sheet.cell_value(j,11) == 1):
            if prob_sheet.cell_value(j, 3) == 'True':
                AllCorrectProgs[name_c]['mismatch1'] += 1
            else:
                if prob_sheet.cell_value(j, 9) == 'Add':
                    AllCorrectProgs[name_c]['min_loc_added'] = min(AllCorrectProgs[name_c]['min_loc_added'], int(prob_sheet.cell_value(j, 10)))
                    AllCorrectProgs[name_c]['max_loc_added'] = max(AllCorrectProgs[name_c]['max_loc_added'], int(prob_sheet.cell_value(j, 10)))
                elif prob_sheet.cell_value(j, 9) == 'Del':
                    AllCorrectProgs[name_c]['min_loc_rem'] = min(AllCorrectProgs[name_c]['min_loc_rem'], int(prob_sheet.cell_value(j, 10)))
                    AllCorrectProgs[name_c]['max_loc_rem'] = max(AllCorrectProgs[name_c]['max_loc_rem'], int(prob_sheet.cell_value(j, 10)))
                if (prob_sheet.cell_value(j, 4) == 'Yes'):
                    Progs[name_c].add(name)
                    AllCorrectProgs[name_c]['corr_rep1'] += 1
                    AllCorrectProgs[name_c]['min_cost1'] = min(AllCorrectProgs[name_c]['min_cost1'], float(prob_sheet.cell_value(j, 12)))
                    AllCorrectProgs[name_c]['max_cost1'] = max(AllCorrectProgs[name_c]['max_cost1'], float(prob_sheet.cell_value(j, 12)))
        
        # edges + labels + incorr prog edges
        elif (prob_sheet.cell_value(j,11) == 2):
            if prob_sheet.cell_value(j, 3) == 'True':
                AllCorrectProgs[name_c]['mismatch2'] += 1
            else:
                if prob_sheet.cell_value(j, 9) == 'Add':
                    AllCorrectProgs[name_c]['min_loc_added'] = min(AllCorrectProgs[name_c]['min_loc_added'], int(prob_sheet.cell_value(j, 10)))
                    AllCorrectProgs[name_c]['max_loc_added'] = max(AllCorrectProgs[name_c]['max_loc_added'], int(prob_sheet.cell_value(j, 10)))
                elif prob_sheet.cell_value(j, 9) == 'Del':
                    AllCorrectProgs[name_c]['min_loc_rem'] = min(AllCorrectProgs[name_c]['min_loc_rem'], int(prob_sheet.cell_value(j, 10)))
                    AllCorrectProgs[name_c]['max_loc_rem'] = max(AllCorrectProgs[name_c]['max_loc_rem'], int(prob_sheet.cell_value(j, 10)))
                if (prob_sheet.cell_value(j, 4) == 'Yes'):
                    Progs[name_c].add(name)
                    AllCorrectProgs[name_c]['corr_rep2'] += 1
                    AllCorrectProgs[name_c]['min_cost2'] = min(AllCorrectProgs[name_c]['min_cost2'], float(prob_sheet.cell_value(j, 12)))
                    AllCorrectProgs[name_c]['max_cost2'] = max(AllCorrectProgs[name_c]['max_cost2'], float(prob_sheet.cell_value(j, 12)))
        # labels + corr prog edges
        elif (prob_sheet.cell_value(j,11) == 3):
            if prob_sheet.cell_value(j, 3) == 'True':
                AllCorrectProgs[name_c]['mismatch3'] += 1
            else:
                if prob_sheet.cell_value(j, 9) == 'Add':
                    AllCorrectProgs[name_c]['min_loc_added'] = min(AllCorrectProgs[name_c]['min_loc_added'], int(prob_sheet.cell_value(j, 10)))
                    AllCorrectProgs[name_c]['max_loc_added'] = max(AllCorrectProgs[name_c]['max_loc_added'], int(prob_sheet.cell_value(j, 10)))
                elif prob_sheet.cell_value(j, 9) == 'Del':
                    AllCorrectProgs[name_c]['min_loc_rem'] = min(AllCorrectProgs[name_c]['min_loc_rem'], int(prob_sheet.cell_value(j, 10)))
                    AllCorrectProgs[name_c]['max_loc_rem'] = max(AllCorrectProgs[name_c]['max_loc_rem'], int(prob_sheet.cell_value(j, 10)))
                if (prob_sheet.cell_value(j, 4) == 'Yes'):
                    AllCorrectProgs[name_c]['corr_rep3'] += 1
                    AllCorrectProgs[name_c]['min_cost3'] = min(AllCorrectProgs[name_c]['min_cost3'], float(prob_sheet.cell_value(j, 12)))
                    AllCorrectProgs[name_c]['max_cost3'] = max(AllCorrectProgs[name_c]['max_cost3'], float(prob_sheet.cell_value(j, 12)))
                    Progs[name_c].add(name)
        if (prob_sheet.cell_value(j, 8) == 'Yes'):
            AllCorrectProgs[name_c]['timeouts'] += 1
        if (prob_sheet.cell_value(j, 2) == 'Yes'):
            AllCorrectProgs[name_c]['reps'] += 1
        if (prob_sheet.cell_value(j, 4) == 'Yes'):
            AllCorrectProgs[name_c]['correct_reps'] += 1
        if (prob_sheet.cell_value(j, 4) == 'Partial'):
            AllCorrectProgs[name_c]['partial_reps'] += 1
        if (prob_sheet.cell_value(j, 6) == 'Yes'):
            AllCorrectProgs[name_c]['parse_err'] += 1
for c in AllCorrectProgs:
    sheet1.write(i, 0, c)
    sheet1.write(i, 1, AllCorrectProgs[c]['reps'])
    sheet1.write(i, 2, AllCorrectProgs[c]['correct_reps'])
    sheet1.write(i, 3, AllCorrectProgs[c]['partial_reps'])
    sheet1.write(i, 4, AllCorrectProgs[c]['mismatch0'])
    sheet1.write(i, 5, AllCorrectProgs[c]['mismatch1'])
    sheet1.write(i, 6, AllCorrectProgs[c]['mismatch2'])
    sheet1.write(i, 7, AllCorrectProgs[c]['mismatch3'])
    sheet1.write(i, 8, AllCorrectProgs[c]['max_loc_rem'])
    sheet1.write(i, 9, AllCorrectProgs[c]['min_loc_rem'])
    sheet1.write(i, 10, AllCorrectProgs[c]['max_loc_added'])
    sheet1.write(i, 11, AllCorrectProgs[c]['min_loc_added'])
    sheet1.write(i, 12, AllCorrectProgs[c]['parse_err'])
    if AllCorrectProgs[c]['max_cost'] != 0:
        sheet1.write(i, 13, AllCorrectProgs[c]['max_cost'])
    if AllCorrectProgs[c]['min_cost'] != 99999999:
        sheet1.write(i, 14, AllCorrectProgs[c]['min_cost'])
    if AllCorrectProgs[c]['max_cost1'] != 0:
        sheet1.write(i, 15, AllCorrectProgs[c]['max_cost1'])
    if AllCorrectProgs[c]['min_cost1'] != 99999999:
        sheet1.write(i, 16, AllCorrectProgs[c]['min_cost1'])
    if AllCorrectProgs[c]['max_cost2'] != 0:
        sheet1.write(i, 17, AllCorrectProgs[c]['max_cost2'])
    if AllCorrectProgs[c]['min_cost2'] != 99999999:
        sheet1.write(i, 18, AllCorrectProgs[c]['min_cost2'])
    if AllCorrectProgs[c]['max_cost3'] != 0:
        sheet1.write(i, 19, AllCorrectProgs[c]['max_cost3'])
    if AllCorrectProgs[c]['min_cost3'] != 99999999:
        sheet1.write(i, 20, AllCorrectProgs[c]['min_cost3'])
    sheet1.write(i, 21, AllCorrectProgs[c]['timeouts'])
    sheet1.write(i, 22, AllCorrectProgs[c]['runs'])
    sheet1.write(i, 23, AllCorrectProgs[c]['corr_rep0'])
    sheet1.write(i, 24, AllCorrectProgs[c]['corr_rep1'])
    sheet1.write(i, 25, AllCorrectProgs[c]['corr_rep2'])
    sheet1.write(i, 26, AllCorrectProgs[c]['corr_rep3'])
    sheet1.write(i,27,AllCorrectProgs[c]['testcase'])
    i += 1

wb.save('1554A_corr_1.xls')
Progs = {k: v for k, v in sorted(Progs.items(), key=lambda item: len(item[1]), reverse=True)}
corr = []
tot = set()
for p in Progs:
    temp = tot.union(Progs[p])
    if len(temp) > len(tot):
        corr += [p]
        tot = temp
    if len(tot) >=82:
        break
print(Progs)
print('\n', corr, '\n', len(corr))