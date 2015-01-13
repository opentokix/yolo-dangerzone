#include <linux/module.h>
#include <linux/kernel.h>
int init_module(void)
{
    struct timeval t;
    struct tm broken;
    do_gettimeofday(&t);
    time_to_tm(t.tv_sec, 0, &broken);
    
    printk(KERN_INFO "-- MARK -- Added manually at: %ld-%02d-%02d %02d:%02d:%02d\n", 1900 + broken.tm_year, 
                                                                          broken.tm_mon + 1, 
                                                                          broken.tm_mday, 
                                                                          broken.tm_hour, 
                                                                          broken.tm_min, 
                                                                          broken.tm_sec);

    
    return 0;
}

void cleanup_module(void)
    {
    }
