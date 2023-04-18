#ifndef PRINT_MODULE_H
#define PRINT_MODULE_H

#define Module_load_success_message "Output stream module load: success\n"
#define Log_prefix "[LOG]"

/*
    input:  printchar-callback, current_time, log message
    output: void
    result: "Log_prefix current_time message"
*/
void print_log(char (*print)(char), char* current_time, char* message);

char print_char(char ch);

#endif  // PRINT_MODULE_H