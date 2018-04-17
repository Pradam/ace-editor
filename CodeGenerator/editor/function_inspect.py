import inspect
import os
import importlib

def get_functions(libraries):

    functions = {}    
    for lib in libraries:
        try:
             imported_library = importlib.import_module(lib)
        except:
            print ('Error Importing library "%s" during resolving methods' % lib)
            continue
        resolved_classes = inspect.getmembers(imported_library,predicate=inspect.isclass)
        
        if resolved_classes:
            for class_name in resolved_classes:
                try:
                    imported_object = getattr(imported_library,class_name[0])
                except ImportError:
                    print ('Error Importing class "%s" of library "%s" during resolving methods' % (class_name[0],lib))
                    continue
                funcs = inspect.getmembers(imported_object,predicate=inspect.ismethod)
                funcs = [ x[0] for x in funcs if '__' not in x[0] ]
                functions.update({class_name[0]:funcs})
    
    return functions	

