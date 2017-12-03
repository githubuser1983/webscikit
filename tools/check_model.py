#!/usr/bin/python
import sys,os
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')
import cPickle as pickle
import hashlib, gzip,shutil

def save(object, filename, protocol = -1):
    """Save an object to a compressed disk file.
       Works well with huge objects.
    """
    file = gzip.GzipFile(filename, 'wb')
    pickle.dump(object, file, protocol)
    file.close()

def load(filename):
    """Loads a compressed object from disk
    """
    file = gzip.GzipFile(filename, 'rb')
    object = pickle.load(file)
    file.close()
    return object

def overwrite_tmp_dir(filename):
    """ Creates tmp-dir based on hash of file given through filename.
        If tmp-dir exists, it will be deleted and created again.
    """
    f = open(filename,"r")
    buf = f.read()
    hasher = hashlib.md5()
    hasher.update(buf)
    dir_name = os.path.join("/tmp/", hasher.hexdigest())
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)
    return dir_name

def copy(from_filename,to_filename):
    """ Copies from_file to to_file.
    """
    from_file = open(from_filename,"rb")
    to_file = open(to_filename,"wb")
    to_file.write(from_file.read())
    from_file.close()
    to_file.close()


if __name__=="__main__":
    model_name = sys.argv[1]
    pkl_file_name = model_name + "_model.pkl"
    py_file_name = model_name + "_model.py"
    try:
        tmp_dir = overwrite_tmp_dir(pkl_file_name)
    except IOError as e:
        print e
        print "Pickled file %s not found. Did you run fit_%s.py in this directory?" % ( pkl_file_name, model_name)
        sys.exit(-1)
    copy(pkl_file_name, os.path.join(tmp_dir,pkl_file_name))
    try:
        copy(py_file_name, os.path.join(tmp_dir,py_file_name))
    except IOError as e:
        print e
        print "Did not find %s in this directory." % py_file_name
        sys.exit(-1)
    #try:
    #    webscikitmodelspath = os.environ["WEBSCIKITMODELSPATH"]
    #except KeyError:
    #    print "environment variable WEBSCIKITMODELSPATH is not set."
    #    sys.exit(-1)
    # overwrite current dir with webscikitpath, so that python does not look in the current dir for additional modules
    #sys.path[0] = webscikitmodelspath
    sys.path[0] = tmp_dir
 
    try:
        model = load(os.path.join(tmp_dir,pkl_file_name))
        attributes = ["metadata", "predict", "transform","transform_predict"]
        for attr in attributes:
            if not hasattr(model,attr):
                print "%s does not have attribute '%s'" % (model_name, attr)
                sys.exit(-1)
        print model.metadata
    except ImportError as e:
        print e
        print "Looks like you have imported from another source as PYTHONPATH. Please do not do this as pickle will not work otherwise"
        sys.exit(-1)
