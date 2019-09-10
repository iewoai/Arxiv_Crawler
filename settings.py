import pickle
import os
import tempfile
from contextlib import contextmanager

class Config(object):
    # main paper information repo file
    search_query = 'cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML'
    # 主url
    api_url = 'http://export.arxiv.org/api/query?'
    # 从何位置开始
    start_index = 0
    # 一次展示多少entry
    max_results = 2
    # 总共循环多少entry
    max_index = 4
    # 排序 默认按日期
    sortBy= 'lastUpdatedDate'
    # 排序方式 降序
    sortOrder= 'descending'
    db_path = 'db.p'
    # 提取延迟
    wait_time = 3.0
    # 
    break_on_no_added = 10

    # intermediate processing folders
    pdf_dir = os.path.join('data', 'pdf')
    #txt_dir = os.path.join('data', 'txt')
    thumbs_dir = os.path.join('data', 'thumbs')
    # intermediate pickles
    #tfidf_path = 'tfidf.p'
    #meta_path = 'tfidf_meta.p'
    #sim_path = 'sim_dict.p'
    #user_sim_path = 'user_sim.p'
    # sql database file
    #db_serve_path = 'db2.p' # an enriched db.p with various preprocessing info
    #database_path = 'as.db'
    #serve_cache_path = 'serve_cache.p'
    
    #beg_for_hosting_money = 1 # do we beg the active users randomly for money? 0 = no.
    #banned_path = 'banned.txt' # for twitter users who are banned
    tmp_dir = 'tmp'

# 储存解析的所有信息
def safe_pickle_dump(obj, fname):
    with open_atomic(fname, 'wb') as f:
        pickle.dump(obj, f, -1)

@contextmanager
def _tempfile(*args, **kws):
    """ Context for temporary file.

    Will find a free temporary filename upon entering
    and will try to delete the file on leaving

    Parameters
    ----------
    suffix : string
        optional file suffix
    """
    fd, name = tempfile.mkstemp(*args, **kws)
    os.close(fd)
    try:
        # print('1')
        yield name
    finally:
        try:
            os.remove(name)
            # print(name)
        except OSError as e:
            if e.errno == 2:
                pass
            else:
                raise e


@contextmanager
def open_atomic(filepath, *args, **kwargs):
    """ Open temporary file object that atomically moves to destination upon
    exiting.

    Allows reading and writing to and from the same filename.

    Parameters
    ----------
    filepath : string
        the file path to be opened
    fsync : bool
        whether to force write the file to disk
    kwargs : mixed
        Any valid keyword arguments for :code:`open`
    """
    fsync = kwargs.pop('fsync', False)

    with _tempfile(dir=os.path.dirname(filepath)) as tmppath:
        # print(tmppath)
        with open(tmppath, *args, **kwargs) as f:
            yield f
            if fsync:
                f.flush()
                os.fsync(f.fileno())
        os.remove(filepath)
        os.rename(tmppath, filepath)

def safe_pickle_dump(obj, fname):
    with open_atomic(fname, 'wb') as f:
        pickle.dump(obj, f, -1)