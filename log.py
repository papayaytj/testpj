#!/usr/bin/python

import logging , sys

if __name__=="__main__":
    """
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='app.log', filemode='w')

    
    
    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')
    logging.error('This is error message')
    logging.critical('This is critical message')
    for i in range(0,10):
        logging.info(str(i))
    """
    logger = logging.getLogger('mylogger')  
    logger.setLevel(logging.DEBUG)  
      
    fh = logging.FileHandler('app.log')  
    fh.setLevel(logging.DEBUG)  
        
    #ch = logging.StreamHandler()  
    #ch.setLevel(logging.DEBUG)  
          
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  
    #ch.setFormatter(formatter)  

    logger.addHandler(fh)  
    #logger.addHandler(ch)  
        
    logger.info('foorbar')  
