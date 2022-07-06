from flask import current_app
import glob

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
 
def check_shp(path, subs = ['.shx','.dbf', 'shp']):
    """
    check if in the folder (path) shp. shx and dbf are present, if so return True, else return False 
    """
    #lista = [L.endswith(i) for L in list_of_file for  i in subs]
    necessary_files = []
    for ext in subs:
        necessary_files.append(glob.glob(f"{path}/*{ext}")) if glob.glob(f"{path}/*{ext}") else None
    
    if len(necessary_files) > 2:
        return True

    return False

    

