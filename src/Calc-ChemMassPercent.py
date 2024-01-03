#!/usr/bin/env python3
#coding: utf-8

#
# Calc-ChemMassPercent
#

import io, sys, os
import re
import argparse

_version = "Wed Jan  3 04:47:04 TST 2024"
_code    = "MyCommands(LINUX+WINDOWS/PYTHON3/UTF-8)"

## switch stdio by platform
if os.name == 'nt':
    ## on windows
    sys.stdin  = io.TextIOWrapper(sys.stdin.buffer,  encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
elif os.name == 'posix':
    ## on linux
    sys.stdin  = open('/dev/stdin',  'r', encoding='utf-8')

def raise_error(msg, *arg):
    scriptfile = os.path.basename(__file__)
    errorheader = "Error[" + scriptfile + "]:"
    print(errorheader, msg.format(arg), file=sys.stderr)
    sys.exit(1)

def get_args():
    help_desc_msg ="""Calc-ChemMassPercent - Recalculate the mass percent concentration

    Synopsis:
        Calculate mass percent concentration when mixing multiple solutions.
    
        python Calc-ChemMassPercent.py -f "100 mL : 0.3 NaCl, 0.03 T-N + 100 mL : 3.0% T-N +200 mL" -r 2

            Type          : Solution.1
            Formula       : 100 mL : 0.3 NaCl, 0.03 T-N
            Volume        : 100 mL
            NaCl          : 30.0 g / 100 mL = 0.30 (30.00 %)
            T-N           : 3.0 g / 100 mL = 0.03 (3.00 %)

            Type          : Solution.2
            Formula       : 100 mL : 3.0% T-N
            Volume        : 100 mL
            T-N           : 3.0 g / 100 mL = 0.03 (3.00 %)

            Type          : Solution.3
            Formula       : 200 mL
            Volume        : 200 mL

            Type          : Product
            Formula       : 100mL:0.3NaCl,0.03T-N + 100mL:3.0%T-N + 200mL
            Total_Volume  : 400.0 mL
            Total_NaCl    : 30.0 g / 400.0 mL = 0.07 (7.50 %)
            Total_T-N     : 6.0 g / 400.0 mL = 0.01 (1.50 %)
            Total_Solid_@ : 36.0 g / 400.0 mL = 0.09 (9.00 %)

    Usage:
        'solution.1 + solution.2 + ...' | python Calc-ChemMassPercent.py
        python Calc-ChemMassPercent.py -f 'solution.1 + solution.2 + ...'

    Expression pattern:
        Basic:
            Volume             -> 100
            Volume : Percent % -> 100 : 3 %
            Volume : Ratio     -> 100 : 0.3

            <Rule>
            - Allows specification of solute only
              (Example at the top of the list)

        With Unit:
            Volume [unit]                 -> 100 mL
            Volume [unit] : w/v Percent % -> 100 mL : 3 %
            Volume [unit] : Ratio         -> 100 mL : 0.3

            Weight [unit]                 -> 100 kg
            Weight [unit] : w/w Percent % -> 100 kg : 3 %
            Weight [unit] : Ratio         -> 100 kg : 0.3

            <Note>
            - The Solute units must be the same throughout the formula.
              (If a unit difference detected, an error will be returned)
        
        With Solvent name:
            Volume : Percent % Name -> 100 : 3 % NaCl
            Volume : Ratio Name     -> 100 : 0.3 NaCl
        
        Mix Multiple Solutions with different concentrations (use the '+'):
            -> 100:3% + 100:1%
            -> 100mL:3%NaCl + 100mL:1%NaCl

            <Note>
            - Add up solvents with the same name.
            - If the solvents name is omitted, the names
              M1, M2, ... are automatically assigned from the left.
        
        Solutions containing multiple Solvents (use ",")
            -> 100 : 10%, 3%
            -> 100 mL : 10% NaCl, 3% T-N

            <Note>
            - You can add as many Solvents as you want.
        
        Solvent can be specified by solid content.
            -> 100 mL + 0 mL : 15.0 NaCl (add 15g of NaCl)
            -> 100 mL + 0 : 15.0 (add 15g of Something)

            <Note>
            In this case, if the total volume of aqueous solution
            in the formula is zero, a "div/0" error will be returned.
        
        Practice:
            <Q.1>
            Dilute 100mL of 3w/v% NaCl solution
            to double volume with water.

                100 mL : 3% NaCl + 100 mL
                100 mL : 0.3 NaCl + 100 mL
                100 : 3% + 100
                100 : 0.3 + 100

            <Q.2>
            An aqueous solution weighing 100g containing
            10w/w% NaCl and 3w/w%T-N as a solvent.

                100 g : 10% NaCl, 3% T-N
                100 g : 0.1 NaCl, 0.03 T-N
                100 : 10%, 3%
                100 : 0.1, 0.03

                "/","*" can be used for concentration term,
                but do not use "+" because it is used to
                express mixtures of Solutions:

                100 : 10%, 3% = 100 : 10/100, 3/100*1.0

    Thanks:
        MathPython
        https://wiki3.jp/MathPython/page/34
    
    Links:
        Calc-ChemMassPercent.py, Calc-ChemWeightLR.py,
        Get-PeriodicTable.py, Get-MolecularMass.py,
        Calc-ChemMassPercent.py

    """
    help_epi_msg = """EXAMPLES:

    # Dilute a solvent with a weight of 100
    # in which 15 w/w% of something (Mat.1) is dissolved
    # with the same weight of water.
    
    python Calc-ChemMassPercent.py -f "100:0.15+100"

        Type          : Solution.1
        Formula       : 100:0.15
        Volume        : 100
        Mat.1         : 15.0 / 100 = 0.150 (15.000 %)

        Type          : Solution.2
        Formula       : 100
        Volume        : 100

        Type          : Product
        Formula       : 100:0.15 + 100
        Total_Volume  : 200.0
        Total_Mat.1   : 15.0 / 200.0 = 0.075 (7.500 %)
        Total_Solid_@ : 15.0 / 200.0 = 0.075 (7.500 %)
    
    # Dissolve 15.0g of salt in 100g of saline solution
    # with a concentration of 10 w/w%

    python Calc-ChemMassPercent.py -f "100 mL : 0.1 NaCl + 0 mL : 15.0 NaCl"

        Type          : Solution.1
        Formula       : 100 mL : 0.1 NaCl
        Volume        : 100 mL
        NaCl          : 10.0 g / 100 mL = 0.100 (10.000 %)

        Type          : Solution.2
        Formula       : 0 mL : 15.0 NaCl
        Volume        : 0
        NaCl          : 15.000 g

        Type          : Product
        Formula       : 100mL:0.1NaCl + 0:15.0NaCl
        Total_Volume  : 100.0 mL
        Total_NaCl    : 25.0 g / 100.0 mL = 0.250 (25.000 %)
        Total_Solid_@ : 25.0 g / 100.0 mL = 0.250 (25.000 %)

    # Calculate mass percent concentration when mixing multiple solutions.
    "100 L : 3.0% NaCl + 100 L : 9.0% NaCl + 200" | python Calc-ChemMassPercent.py
    # or
    python Calc-ChemMassPercent.py -f "100 L : 3.0% NaCl + 100 L : 9.0% NaCl + 200"

        Type          : Solution.1
        Formula       : 100 L : 3.0% NaCl
        Volume        : 100 L
        NaCl          : 3.0 kg / 100 L = 0.03 (3.00 %)

        Type          : Solution.2
        Formula       : 100 L : 9.0% NaCl
        Volume        : 100 L
        NaCl          : 9.0 kg / 100 L = 0.09 (9.00 %)

        Type          : Solution.3
        Formula       : 200
        Volume        : 200

        Type          : Product
        Formula       : 100L:3.0%NaCl + 100L:9.0%NaCl + 200
        Total_Volume  : 400.0 L
        Total_NaCl    : 12.0 kg / 400.0 L = 0.03 (3.00 %)
        Total_Solid_@ : 12.0 kg / 400.0 L = 0.03 (3.00 %)

    # -v, --verbose option: Output total solvent weight for each step
    python Calc-ChemMassPercent.py -f "100 L : 3.0% NaCl + 100 L : 9.0% NaCl + 200" -v

        Type          : Solution.1
        Formula       : 100 L : 3.0% NaCl
        Volume        : 100 L
        NaCl          : 3.0 kg / 100 L = 0.030 (3.000 %)
        Total_Volume  : 100.0 L
        Total_Solid_@ : 3.0 kg / 100.0 L = 0.030 (3.000 %)
        Total_NaCl    : 3.0 kg / 100.0 L = 0.030 (3.000 %)

        Type          : Solution.2
        Formula       : 100 L : 9.0% NaCl
        Volume        : 100 L
        NaCl          : 9.0 kg / 100 L = 0.090 (9.000 %)
        Total_Volume  : 200.0 L
        Total_Solid_@ : 12.0 kg / 200.0 L = 0.060 (6.000 %)
        Total_NaCl    : 12.0 kg / 200.0 L = 0.060 (6.000 %)

        Type          : Solution.3
        Formula       : 200
        Volume        : 200
        Total_Volume  : 400.0 L
        Total_Solid_@ : 12.0 kg / 400.0 L = 0.030 (3.000 %)
        Total_NaCl    : 12.0 kg / 400.0 L = 0.030 (3.000 %)

        Type          : Product
        Formula       : 100L:3.0%NaCl + 100L:9.0%NaCl + 200
        Total_Volume  : 400.0 L
        Total_NaCl    : 12.0 kg / 400.0 L = 0.030 (3.000 %)
        Total_Solid_@ : 12.0 kg / 400.0 L = 0.030 (3.000 %)

    # Simple expression: Mix 100g of 3w/w% saline and 100g of 9w/w% saline:

    python Calc-ChemMassPercent.py -f "100g:3% + 100g:9%"

        Type          : Solution.1
        Formula       : 100g:3%
        Volume        : 100 g
        Mat.1         : 3.0 g / 100 g = 0.030 (3.000 %)

        Type          : Solution.2
        Formula       : 100g:9%
        Volume        : 100 g
        Mat.1         : 9.0 g / 100 g = 0.090 (9.000 %)

        Type          : Product
        Formula       : 100g:3% + 100g:9%
        Total_Volume  : 200.0 g
        Total_Mat.1   : 12.0 g / 200.0 g = 0.060 (6.000 %)
        Total_Solid_@ : 12.0 g / 200.0 g = 0.060 (6.000 %)
    
    # Mixing multiple solutions containing multiple solvents
    python Calc-ChemMassPercent.py -f "100 mL : 0.3 NaCl, 0.03 T-N + 100 mL : 3.0% T-N +200 mL" -r 2
    
        Type          : Solution.1
        Formula       : 100 mL : 0.3 NaCl, 0.03 T-N
        Volume        : 100 mL
        NaCl          : 30.0 g / 100 mL = 0.30 (30.00 %)
        T-N           : 3.0 g / 100 mL = 0.03 (3.00 %)

        Type          : Solution.2
        Formula       : 100 mL : 3.0% T-N
        Volume        : 100 mL
        T-N           : 3.0 g / 100 mL = 0.03 (3.00 %)

        Type          : Solution.3
        Formula       : 200 mL
        Volume        : 200 mL

        Type          : Product
        Formula       : 100mL:0.3NaCl,0.03T-N + 100mL:3.0%T-N + 200mL
        Total_Volume  : 400.0 mL
        Total_NaCl    : 30.0 g / 400.0 mL = 0.07 (7.50 %)
        Total_T-N     : 6.0 g / 400.0 mL = 0.01 (1.50 %)
        Total_Solid_@ : 36.0 g / 400.0 mL = 0.09 (9.00 %)
    """

    parser = argparse.ArgumentParser(description=help_desc_msg,
                    epilog=help_epi_msg,
                    formatter_class=argparse.RawDescriptionHelpFormatter)
    #parser = argparse.ArgumentParser(description='calc matrix using numpy')
    #parser.print_help()
    ts = lambda x:list(map(str, x.split(';')))
    parser.add_argument("-f", "--formula", help="molecular formula", type=ts)
    parser.add_argument("-r", "--round", help="round", default="3", type=str)
    parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
    parser.add_argument("-d", "--debug", help="debug", action="store_true")
    parser.add_argument("-V", "--version", help="version", action="version", version=_version)
    args = parser.parse_args()
    return(args)

def open_file(mode = 'r'):
    out_lines = []
    readfile = sys.stdin
    for line in readfile:
        line = line.rstrip('\r\n')
        for l in line.split(";"):
            out_lines.append(str(l).strip())
    return out_lines

def strip_formulas(formulas):
    out_lines = []
    for f in formulas:
        out_lines.append(str(f))
    return out_lines

def isNumber(string):
    test_str = str(string)
    try:
        float(test_str)
    except ValueError:
        return False
    else:
        return True

def splitTermToNumAndUnit(term, compiled_regex):
    str_num  = compiled_regex.sub(r'\1', term)
    str_num  = str_num.replace(',', '').replace('_', '').rstrip('-/*')
    str_unit = compiled_regex.sub(r'\2', term)
    if re.search(r'\*|\/', str_num):
        str_num = str(eval(str_num))
    if str_unit == '':
        pass
    elif not isNumber(str_num):
        raise_error("Could not get Volume from '{}'.".format(term))
        sys.exit(1)
    return str_num, str_unit

def getSolventUnit(unit):
    if unit == '':
        ret = r''
    elif unit.lower() == r'kL'.lower():
        ret = r't'
    elif unit.lower() == r'L'.lower():
        ret = r'kg'
    elif unit.lower() == r'mL'.lower():
        ret = r'g'
    elif unit.lower() == r'kg'.lower():
        ret = unit
    elif unit.lower() == r'g'.lower():
        ret = unit
    elif unit.lower() == r'mg'.lower():
        ret = unit
    else:
        ret = unit
    return ret

class TotalVolume:

    def __init__(self, solute_volume = 0, unit = None, name = None):
        self.name = name
        self.unit = unit
        self.solute_volume = solute_volume
    
    def sumSoluteVolume(self, add_volume, unit):
        # test unit
        if self.testUnit(unit):
            self.solute_volume += add_volume
        else:
            raise_error("Deferent unit detected. '{}' and '{}'".format(unit, self.unit))

    def getSoluteVolume(self):
        return self.solute_volume

    def testUnit(self, unit):
        if unit == None or unit == '':
            return True
        elif unit.lower() == self.unit.lower():
            return True
        else:
            return False

class Solution:

    def __init__(self, percent, solute_weight, name = None):
        self.name = name
        self.percent = percent
        self.solute_weight = solute_weight
        self.solvent_weight = self.initSolventWeight()

    def initSolventWeight(self):
        if self.solute_weight == 0:
            ret = (self.percent) * 1
        else:
            ret = (self.percent) * self.solute_weight
            
        return ret
        
    def getSoluteWeight(self):
        ret = self.solute_weight - self.getSolventWeight()
        return ret
    
    def sumSolventWeight(self, percent, solute_weight):
        if solute_weight == 0:
            self.solvent_weight += percent * 1
        else:
            self.solvent_weight += percent * solute_weight

class Solid:

    def __init__(self, percent, solute_weight, sub = 0):
        self.name = "Solid"
        self.percent = percent
        self.solute_weight = solute_weight
        self.solvent_weight = self.initSolidWeight(sub)

    def initSolidWeight(self, sub = 0):
        if self.solute_weight == 0:
            ret = (self.percent * 1) - sub
        else:
            ret = (self.percent * self.solute_weight) - sub
        return ret
    
    def getSolventWeight(self):
        return self.solvent_weight
    
    def getCurrentSolventWeight(self, percent, solute_weight, sub = 0):
        ret = (percent * solute_weight) - sub
        return ret
    
    def sumSolventWeight(self, percent, solute_weight, sub = 0):
        if solute_weight == 0:
            self.solvent_weight += (percent * 1) - sub
        else:
            self.solvent_weight += (percent * solute_weight) - sub

if __name__ == '__main__':
    # get args
    args = get_args()

    # read formula
    formulas = []
    if args.formula:
        formulas = strip_formulas(args.formula)
    else:
        formulas = open_file()

    # set variable
    solid_name = "Solid_@"
    solution_symbol = "Solution."
    term_symbol = "Mat."
    debug_ljust = 13
    line_counter = 0
    # regex
    allowed_num = r'^([-0-9.eE\*/,_]+)'
    allowed_num_and_percent = r'^([-0-9.eE\*/,_]+)%(.*)$'
    separate_num_and_unit   = r'^([-0-9.eE\*/,_]+)(.*)$'
    regex_allowed_num = re.compile(allowed_num)
    regex_allowed_num_and_percent = re.compile(allowed_num_and_percent)
    regex_separate_num_and_unit = re.compile(separate_num_and_unit)
    # lists
    solution_dict = {}
    solvent_dict  = {}
    for fml in formulas:
        # formula counter
        line_counter += 1
        # get formula
        fml = fml.rstrip('\r\n')
        fml = fml.strip()
        # test formula
        if re.search('^$', fml):
            sys.exit(0)
        if not regex_allowed_num.search(fml):
            sys.exit(0)
        #if args.debug or args.verbose:
        #    print("{} : {}".format("Input".ljust(debug_ljust), fml.replace(' ', '').replace('+', ' + ')))
        #    print("")
        # split formula into solutions with "+" symbol
        solution_counter = 0
        solutions = fml.split(r'+')
        term_len = len(solutions)
        if True:
            # init solid class
            solvent_dict[solid_name] = Solid(0, 0)
        for solution in solutions:
            solution = solution.strip()
            solution_counter += 1
            solution_id = solution_symbol + str(solution_counter)
            if True:
                print("{} : {}".format("Type".ljust(debug_ljust), solution_id))
                print("{} : {}".format("Formula".ljust(debug_ljust), solution))
            # get Volume and mass percent concentration
            solution = solution.replace(' ', '')
            if re.search(r':', solution):
                # Volume and Concentration
                # e.g. "1000 L : 0.3 NaCl, 0.03 T-N"
                vol  = re.sub(r'^([^:]*):(.*)$', r'\1', solution).strip()
                if vol == '': vol = str(0)
                conc = re.sub(r'^([^:]*):(.*)$', r'\2', solution).strip()
            else:
                # Volume only
                # e.g. "1000 L"
                vol  = str(solution).strip()
                conc = str('')
            # set solution volume and unit
            str_vol, str_vol_unit = splitTermToNumAndUnit(vol, regex_separate_num_and_unit)
            if solution_counter == 1:
                # init volume
                total_volume = TotalVolume(float(str_vol), str_vol_unit)
                if str_vol_unit == "":
                    print_solution_unit = r''
                    print_solvent_unit  = r''
                else:
                    print_solution_unit = str_vol_unit
                    print_solvent_unit  = getSolventUnit(str_vol_unit)
            else:
                # add volume
                total_volume.sumSoluteVolume(float(str_vol), str_vol_unit)
            if True:
                if print_solution_unit == '':
                    print("{} : {}".format("Volume".ljust(debug_ljust), str_vol))
                else:
                    print("{} : {} {}".format("Volume".ljust(debug_ljust), str_vol, str_vol_unit))
            # get each mass percent concentration nums
            if conc == '':
                # no conc terms (Volume only)
                conc_terms = ['']
                conc_terms_len = 0
            else:
                conc_terms = conc.split(r',')
                conc_terms_len = len(conc_terms)
            # set solvent name and concentration
            term_counter = 0
            for cterm in conc_terms:
                # interpret % symbol
                cterm = cterm.strip()
                if cterm == '':
                    continue
                term_counter += 1
                if regex_allowed_num_and_percent.search(cterm):
                    cterm = regex_allowed_num_and_percent.sub(r'\1/100\2', cterm)
                str_solv_num, str_solv_name = splitTermToNumAndUnit(cterm, regex_separate_num_and_unit)
                if str_solv_name == '':
                    str_solv_name = term_symbol + str(term_counter)
                # add to dict
                if str_solv_name in solvent_dict.keys():
                    # add solvent weight
                    solvent_dict[str_solv_name].sumSolventWeight(float(str_solv_num), float(str_vol))
                else:
                    # init solvent dict
                    solvent_dict[str_solv_name] = Solution(float(str_solv_num), float(str_vol), str(str_solv_name))
                if True:
                    solvent_dict[solid_name].sumSolventWeight(float(str_solv_num), float(str_vol))
                # output each solvent mass percent
                if True:
                    c = str_solv_name.ljust(debug_ljust)
                    v = str_vol
                    n = float(str_solv_num)
                    p = float(str_solv_num) * 100
                    w = n * float(v)
                    n = str("{:." + args.round + "f}").format(n)
                    p = str("{:." + args.round + "f}").format(p)
                    if print_solution_unit == '':
                        if float(v) == 0:
                            # case Volume == 0 (only solvent)
                            w = n * 1
                            print(str("{} : {}").format(c, w))
                        else:
                            print(str("{} : {} / {} = {} ({} %)").format(c, w, v, n, p))
                    else:
                        u_solv = print_solvent_unit
                        u_solu = print_solution_unit
                        if float(v) == 0:
                            # case Volume == 0 (only solvent)
                            w = n * 1
                            print(str("{} : {} {}").format(c, w, u_solv))
                        else:
                            print(str("{} : {} {} / {} {} = {} ({} %)").format(c, w, u_solv, v, u_solu, n, p))
            
            if args.debug or args.verbose:
                if print_solution_unit == '':
                    print("{} : {}".format("Total_Volume".ljust(debug_ljust), total_volume.getSoluteVolume()))
                else:
                    print("{} : {} {}".format("Total_Volume".ljust(debug_ljust), total_volume.getSoluteVolume(), print_solution_unit))
                if len(solvent_dict) > 0:
                    for key in solvent_dict.keys():
                        c = str("Total_" + key).ljust(debug_ljust)
                        v = total_volume.getSoluteVolume()
                        w = solvent_dict[key].solvent_weight
                        r = w / v
                        p = w / v * 100
                        r = str("{:." + args.round + "f}").format(r)
                        p = str("{:." + args.round + "f}").format(p)
                        if print_solution_unit == '':
                            print(str("{} : {} / {} = {} ({} %)").format(c, w, v, r, p))
                        else:
                            u_solv = print_solvent_unit
                            u_solu = print_solution_unit
                            print(str("{} : {} {} / {} {} = {} ({} %)").format(c, w, u_solv, v, u_solu, r, p))
            
            if True:
                print("")
        
        # output product
        n = "Total_Volume".ljust(debug_ljust)
        v = total_volume.getSoluteVolume()
        print("{} : {}".format("Type".ljust(debug_ljust), "Product"))
        print("{} : {}".format("Formula".ljust(debug_ljust), fml.replace(' ', '').replace('+', ' + ')))
        if print_solution_unit == '':
            print("{} : {}".format(n, v))
        else:
            u = print_solution_unit
            print("{} : {} {}".format("Total_Volume".ljust(debug_ljust), total_volume.getSoluteVolume(), u))
        if len(solvent_dict) > 0:
            for key in solvent_dict.keys():
                if key != solid_name:
                    c = str("Total_" + key).ljust(debug_ljust)
                    v = total_volume.getSoluteVolume()
                    w = solvent_dict[key].solvent_weight
                    r = w / v
                    p = w / v * 100
                    r = str("{:." + args.round + "f}").format(r)
                    p = str("{:." + args.round + "f}").format(p)
                    if print_solution_unit == '':
                        print(str("{} : {} / {} = {} ({} %)").format(c, w, v, r, p))
                    else:
                        u_solv = print_solvent_unit
                        u_solu = print_solution_unit
                        print(str("{} : {} {} / {} {} = {} ({} %)").format(c, w, u_solv, v, u_solu, r, p))
            key = solid_name
            c = str("Total_" + key).ljust(debug_ljust)
            v = total_volume.getSoluteVolume()
            w = solvent_dict[key].solvent_weight
            r = w / v
            p = w / v * 100
            r = str("{:." + args.round + "f}").format(r)
            p = str("{:." + args.round + "f}").format(p)
            if print_solution_unit == '':
                print(str("{} : {} / {} = {} ({} %)").format(c, w, v, r, p))
            else:
                u_solv = print_solvent_unit
                u_solu = print_solution_unit
                print(str("{} : {} {} / {} {} = {} ({} %)").format(c, w, u_solv, v, u_solu, r, p))
    
    sys.exit(0)
