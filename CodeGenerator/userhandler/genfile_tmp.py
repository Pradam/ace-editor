from log import logging as logg
import subprocess
import copy
import os
import re
def generate_test_suite_file(teststeps,ws_name,ws_ip,ws_uname,ws_passwd,ts_name,library,keyword,variable):
    make_new_template(ts_name)
    fp = open("userhandler/" + ts_name + ".robot", "a") 
    add_library_path(library,ts_name,fp)
    #add_keyword_path(keyword,ts_name)

    ln_testcase = teststeps.split("\n")
    if ln_testcase[-1] != "":
        ln_testcase.append("")
    test_steps = []
    new_testcase = []
    for teststep in ln_testcase:
        logg.warning("testcase %s" % teststep)
        if teststep == "":
            test_steps.append(new_testcase) 
            logg.warning("test_steps %s" % test_steps)
            new_testcase = []
        else:
            new_testcase.append(teststep)

    if len(test_steps) == 0:
        test_steps.append(new_testcase)

    logg.warning("Derived %s" % test_steps)
    tc_no = 0
    
    logg.warning("userhandler/" + ts_name + ".robot")
    fp.write("*** Test Case ***\n")
    fp.flush()
    fp.close()
    
    for testcase in test_steps:
        tsteps = verify_step_params(testcase)
        final_steps = replace_id_for_name(tsteps)
        tc_no = tc_no + 1
        write_testcase(final_steps, tc_no,ts_name)

    logg.warning("Generation Done ")
    return True

def add_library_path(library,ts_name):

    if len(library) == 0:
        logg.warning("Nothing Generation Done ")
        return None

    logg.warning("Library Generation Done ")
    fp = open("userhandler/" + ts_name + ".robot", "a") 
    fp.write("*** Setting ***    Value\n\n" + "Library           ${ProductTarget}/libs/python/lib/PublicAPI.py   scg_ip=10.110.219.42  pubapi_version=v5_0\n") 
    for lib in library:
        lib_list = lib.split("|")
        path=lib_list[1]
        libname=lib_list[0]
        fp.write("Library           "+path+"."+libname+"\n")

    fp.flush()
    fp.close()

def add_keyword_path(keyword,ts_name):

    if len(keyword) == 0:
        return None

    fp = open("userhandler/" + ts_name + ".robot", "a") 
    fp.write("\n") 
    for key in keyword:
        key_list = key.split("|")
        path=key_list[1]
        libname=key_list[0]
        fp.write("Resource           "+path+"."+libname+"\n")
    fp.flush()
    fp.close()

def verify_step_params(teststeps):
    tsteps = []
    for steps in teststeps:
        st_steps = steps.split("  ")
        s_steps = copy.deepcopy(st_steps)
        for var in st_steps:
            if re.search("=",var): 
                ln_var = var.strip().split("=")
                if len(ln_var) == 2:
                    if str(ln_var[1]) == "": 
                        s_steps.remove(var)
        tsteps.append("  ".join(s_steps))        
        logg.warning("steps %s" %tsteps)

    return tsteps

def replace_id_for_name(teststeps):
    tsteps = []
    for steps in teststeps:
        st_steps = steps.split("  ")
        s_steps = copy.deepcopy(st_steps)
        insert_get_id = False
        for var in st_steps:
            logg.warning("STEPS %s" %var)
            if re.match("\s*\S*id=",var,re.I):
                ln_var = var.strip().split("=")
                logg.warning("ID STEP %s" %var)
                if len(ln_var) == 2 and ln_var[0] != "ssid":
                    name = ln_var[1]
                    s_steps.remove(var)
                    s_steps.append(ln_var[0] + "=${" + name + "_id}")
                    insert_get_id = True

        if insert_get_id is True:
            tsteps.append("${" + name + "_id}=  get_id_from_name  name=%s" % name)

        tsteps.append("  ".join(s_steps))        
        logg.warning("steps %s" %tsteps)

    return tsteps

def write_testcase(tsteps,tc_id,ts_name):
    logg.warning("test case %s" %tsteps)
    fp = open("userhandler/" + ts_name + ".robot", "a") 
    fp.write("\nTest Case %s\n" % tc_id) 
    for step in tsteps:
        logg.warning("test case %s" %step)
        fp.write("\t" + step + "\n") 
    fp.flush()
    fp.close()

def make_new_template(ts_name):
    process = subprocess.Popen("cp userhandler/tmp.robot " + "userhandler/" + ts_name + ".robot", shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, preexec_fn=os.setsid)
