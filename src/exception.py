import sys

def error_msg_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    name = exc_tb.tb_frame.f_code.co_filename
    line = exc_tb.tb_lineno
    error = str(error)
    error_message = f"Error occured in python script '{name}' line number {line} and error is {error}"
    return error_message
    
class CustomException(Exception):
    def __init__(self,error_msg,error_detail:sys):
        super().__init__(error_msg)    
        self.error_msg = error_msg_detail(error_msg,error_detail=error_detail)
        
    def __str__(self):
        return self.error_msg    
    