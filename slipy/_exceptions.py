import sys

def _print_error(e):
    """Traceback formatter for handled exceptions

    Parameters
    ----------
    e : Exception
        Exception caught in try/except clause

    Example
    -------
    try:
        raise Exception
    except Exception as e:
        _print_error(e)

    """
    string = '\n\t'.join([
            '{0}', # Exception Type
            'filename: {1}', # filename
            'lineno: {2}\n']) # lineno of error

    fname = sys.exc_info()[2].tb_frame.f_code.co_filename
    tb_lineno = sys.exc_info()[2].tb_lineno

    error_type = str(type(e).__name__)
    error_msg = '\n\t'.join(map(repr, e))
    error_str = '{}: {}'.format(error_type, error_msg)
    
    args = (error_str, fname, tb_lineno)
    sys.stderr.write(string.format(*args))
    sys.stderr.flush()

class ContextError(Exception):
    def __init__(self, message=None):
        
        err_str = 'Cannot create object within existing object context'
        if message:
            err_str = '{0}\n\n\t{1}'.format(err_str, message)
            
        Exception.__init__(self, err_str)