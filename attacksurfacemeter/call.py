__author__ = 'kevin'

from attacksurfacemeter.loaders.cflow_line_parser import CflowLineParser
from attacksurfacemeter.loaders.gprof_line_parser import GprofLineParser
from attacksurfacemeter.loaders.javacg_line_parser import JavaCGLineParser

from attacksurfacemeter.environments import Environments


class Call():
    """
        Represents a function/method call in a source code.
    
        Provides a basic functionality for derived classes.
    """

    c_input_functions = ['canonicalize_file_name', 'catgets', 'confstr', 'ctermid', 'cuserid', 'dgettext',
                       'dngettext', 'fgetc', 'fgetc_unlocked', 'fgets', 'fgets_unlocked', 'fpathconf', 'fread',
                       'fread_unlocked', 'fscanf', 'getc', 'getchar', 'getchar_unlocked', 'getc_unlocked',
                       'get_current_dir_name', 'getcwd', 'getdelim', '__getdelim', 'getdelim', 'getdents', 'getenv',
                       'gethostbyaddr', 'gethostbyname', 'gethostbyname2', 'gethostent', 'gethostid', 'getline',
                       'getline', 'getlogin', 'getlogin_r', 'getmsg', 'getopt', '_getopt_internal', 'getopt_long',
                       'getopt_long_only', 'getpass', 'getpmsg', 'gets', 'gettext', 'getw', 'getwd', 'ngettext',
                       'pathconf', 'pread', 'pread64', 'ptsname', 'ptsname_r', 'read', 'readdir', 'readlink', 'readv',
                       'realpath', 'recv', 'recv_from', 'recvmesg', 'scanf', '__secure_getenv', 'signal', 'sysconf',
                       'ttyname', 'ttyname_r', 'vfscanf', 'vscanf']

    c_output_functions = ['dprintf', 'fprintf', 'fputc', 'fputchar_unlocked', 'fputc_unlocked', 'fputs', 'fputs_unlocked',
                        'fwrite', 'fwrite_unlocked', 'perror', 'printf', 'psignal', 'putc', 'putchar', 'putc_unlocked',
                        'putenv', 'putmsg', 'putpmsg', 'puts', 'putw', 'pwrite', 'pwrite64', 'send', 'sendmsg',
                        'sendto', 'setenv', 'sethostid', 'setlogin', 'ungetc', 'vdprintf', 'vfprintf', 'vsyslog',
                        'write', 'writev']

    ## >=@ move this to another file!
    c_standard_library_functions = ['*pthread_getspecific', '*sbrk', '*sem_open', '_exit', '_Exit', '_flushlbf', '_tolower', '_toupper', '__fbufsize', '__flbf', '__fpending', '__fpurge', '__freadable', '__freading', '__fsetlocking', '__fwritable', '__fwriting', '__ppc_get_timebase', '__ppc_get_timebase_freq', '__ppc_mdoio', '__ppc_mdoom', '__ppc_set_ppr_low', '__ppc_set_ppr_med', '__ppc_set_ppr_med_low', '__ppc_yield', '__va_copy', 'a64l', 'abort', 'abs', 'accept', 'access', 'acos', 'acosf', 'acosh', 'acoshf', 'acoshl', 'acosl', 'addmntent', 'addseverity', 'adjtime', 'adjtimex', 'aio_cancel', 'aio_cancel64', 'aio_error', 'aio_error64', 'aio_fsync', 'aio_fsync64', 'aio_init', 'aio_read', 'aio_read64', 'aio_return', 'aio_return64', 'aio_suspend', 'aio_suspend64', 'aio_write', 'aio_write64', 'alarm', 'aligned_alloc', 'alloca', 'alphasort', 'alphasort64', 'argp_error', 'argp_failure', 'argp_help', 'argp_parse', 'argp_state_help', 'argp_usage', 'argz_add', 'argz_add_sep', 'argz_append', 'argz_count', 'argz_create', 'argz_create_sep', 'argz_delete', 'argz_extract', 'argz_insert', 'argz_next', 'argz_replace', 'argz_stringify', 'asctime', 'asctime_r', 'asin', 'asinf', 'asinh', 'asinhf', 'asinhl', 'asinl', 'asprintf', 'assert', 'assert_perror', 'atan', 'atan2', 'atan2f', 'atan2l', 'atanf', 'atanh', 'atanhf', 'atanhl', 'atanl', 'atexit', 'atof', 'atoi', 'atol', 'atoll', 'backtrace', 'backtrace_symbols', 'backtrace_symbols_fd', 'basename', 'basename', 'bcmp', 'bcopy', 'bind', 'bindtextdomain', 'bind_textdomain_codeset', 'brk', 'bsearch', 'btowc', 'bzero', 'cabs', 'cabsf', 'cabsl', 'cacos', 'cacosf', 'cacosh', 'cacoshf', 'cacoshl', 'cacosl', 'calloc', 'canonicalize_file_name', 'carg', 'cargf', 'cargl', 'casin', 'casinf', 'casinh', 'casinhf', 'casinhl', 'casinl', 'catan', 'catanf', 'catanh', 'catanhf', 'catanhl', 'catanl', 'catclose', 'catgets', 'catopen', 'cbc_crypt', 'cbrt', 'cbrtf', 'cbrtl', 'ccos', 'ccosf', 'ccosh', 'ccoshf', 'ccoshl', 'ccosl', 'ceil', 'ceilf', 'ceill', 'cexp', 'cexpf', 'cexpl', 'cfgetispeed', 'cfgetospeed', 'cfmakeraw', 'cfree', 'cfsetispeed', 'cfsetospeed', 'cfsetspeed', 'chdir', 'chmod', 'chmod', 'chown', 'cimag', 'cimagf', 'cimagl', 'clearenv', 'clearerr', 'clearerr_unlocked', 'clock', 'clog', 'clog10', 'clog10f', 'clog10l', 'clogf', 'clogl', 'close', 'closedir', 'closelog', 'confstr', 'conj', 'conjf', 'conjl', 'connect', 'copysign', 'copysignf', 'copysignl', 'cos', 'cosf', 'cosh', 'coshf', 'coshl', 'cosl', 'cpow', 'cpowf', 'cpowl', 'cproj', 'cprojf', 'cprojl', 'CPU_CLR', 'CPU_ISSET', 'CPU_SET', 'CPU_ZERO', 'creal', 'crealf', 'creall', 'creat', 'creat64', 'crypt', 'crypt_r', 'csin', 'csinf', 'csinh', 'csinhf', 'csinhl', 'csinl', 'csqrt', 'csqrtf', 'csqrtl', 'ctan', 'ctanf', 'ctanh', 'ctanhf', 'ctanhl', 'ctanl', 'ctermid', 'ctime', 'ctime_r', 'cuserid', 'dcgettext', 'dcngettext', 'DES_FAILED', 'des_setparity', 'dgettext', 'difftime', 'dirfd', 'dirname', 'div', 'dngettext', 'drand48', 'drand48_r', 'drem', 'dremf', 'dreml', 'DTTOIF', 'dup', 'dup2', 'ecb_crypt', 'ecvt', 'ecvt_r', 'encrypt', 'encrypt_r', 'endfsent', 'endgrent', 'endhostent', 'endmntent', 'endnetent', 'endnetgrent', 'endprotoent', 'endpwent', 'endservent', 'endutent', 'endutxent', 'envz_add', 'envz_entry', 'envz_get', 'envz_merge', 'envz_strip', 'erand48', 'erand48_r', 'erf', 'erfc', 'erfcf', 'erfcl', 'erff', 'erfl', 'err', 'error', 'error_at_line', 'errx', 'execl', 'execle', 'execlp', 'execv', 'execve', 'execvp', 'exit', 'exp', 'exp10', 'exp10f', 'exp10l', 'exp2', 'exp2f', 'exp2l', 'expf', 'expl', 'expm1', 'expm1f', 'expm1l', 'fabs', 'fabsf', 'fabsl', 'fchdir', 'fchmod', 'fchown', 'fclose', 'fcloseall', 'fcntl', 'fcvt', 'fcvt_r', 'fdatasync', 'fdim', 'fdimf', 'fdiml', 'fdopen', 'fdopendir', 'FD_CLR', 'FD_ISSET', 'FD_SET', 'FD_ZERO', 'feclearexcept', 'fedisableexcept', 'feenableexcept', 'fegetenv', 'fegetexcept', 'fegetexceptflag', 'fegetround', 'feholdexcept', 'feof', 'feof_unlocked', 'feraiseexcept', 'ferror', 'ferror_unlocked', 'fesetenv', 'fesetexceptflag', 'fesetround', 'fetestexcept', 'feupdateenv', 'fflush', 'fflush_unlocked', 'fgetc', 'fgetc_unlocked', 'fgetgrent', 'fgetgrent_r', 'fgetpos', 'fgetpos64', 'fgetpwent', 'fgetpwent_r', 'fgets', 'fgets_unlocked', 'fgetwc', 'fgetwc_unlocked', 'fgetws', 'fgetws_unlocked', 'fileno', 'fileno_unlocked', 'finite', 'finitef', 'finitel', 'flockfile', 'floor', 'floorf', 'floorl', 'fma', 'fmaf', 'fmal', 'fmax', 'fmaxf', 'fmaxl', 'fmemopen', 'fmin', 'fminf', 'fminl', 'fmod', 'fmodf', 'fmodl', 'fmtmsg', 'fnmatch', 'fopen', 'fopen64', 'fopencookie', 'fork', 'forkpty', 'fpathconf', 'fpclassify', 'fprintf', 'fputc', 'fputc_unlocked', 'fputs', 'fputs_unlocked', 'fputwc', 'fputwc_unlocked', 'fputws', 'fputws_unlocked', 'fread', 'fread_unlocked', 'free', 'freopen', 'freopen64', 'frexp', 'frexpf', 'frexpl', 'fscanf', 'fseek', 'fseeko', 'fseeko64', 'fsetpos', 'fsetpos64', 'fstat', 'fstat64', 'fsync', 'ftell', 'ftello', 'ftello64', 'ftruncate', 'ftruncate64', 'ftrylockfile', 'ftw', 'ftw64', 'funlockfile', 'futimes', 'fwide', 'fwprintf', 'fwrite', 'fwrite_unlocked', 'fwscanf', 'gamma', 'gammaf', 'gammal', 'gcvt', 'getauxval', 'getc', 'getchar', 'getchar_unlocked', 'getcontext', 'getcwd', 'getc_unlocked', 'getdate', 'getdate_r', 'getdelim', 'getdomainnname', 'getegid', 'getenv', 'geteuid', 'getfsent', 'getfsfile', 'getfsspec', 'getgid', 'getgrent', 'getgrent_r', 'getgrgid', 'getgrgid_r', 'getgrnam', 'getgrnam_r', 'getgrouplist', 'getgroups', 'gethostbyaddr', 'gethostbyaddr_r', 'gethostbyname', 'gethostbyname2', 'gethostbyname2_r', 'gethostbyname_r', 'gethostent', 'gethostid', 'gethostname', 'getitimer', 'getline', 'getloadavg', 'getlogin', 'getmntent', 'getmntent_r', 'getnetbyaddr', 'getnetbyname', 'getnetent', 'getnetgrent', 'getnetgrent_r', 'getopt', 'getopt_long', 'getopt_long_only', 'getpagesize', 'getpass', 'getpeername', 'getpgid', 'getpgrp', 'getpid', 'getppid', 'getpriority', 'getprotobyname', 'getprotobynumber', 'getprotoent', 'getpt', 'getpwent', 'getpwent_r', 'getpwnam', 'getpwnam_r', 'getpwuid', 'getpwuid_r', 'getrlimit', 'getrlimit64', 'getrusage', 'gets', 'getservbyname', 'getservbyport', 'getservent', 'getsid', 'getsockname', 'getsockopt', 'getsubopt', 'gettext', 'gettimeofday', 'getuid', 'getumask', 'getutent', 'getutent_r', 'getutid', 'getutid_r', 'getutline', 'getutline_r', 'getutmp', 'getutmpx', 'getutxent', 'getutxid', 'getutxline', 'getw', 'getwc', 'getwchar', 'getwchar_unlocked', 'getwc_unlocked', 'getwd', 'get_avphys_pages', 'get_current_dir_name', 'get_nprocs', 'get_nprocs_conf', 'get_phys_pages', 'glob', 'glob64', 'globfree', 'globfree64', 'gmtime', 'gmtime_r', 'grantpt', 'grantpt', 'gsignal', 'gtty', 'hasmntopt', 'hcreate', 'hcreate_r', 'hdestroy', 'hdestroy_r', 'hsearch', 'hsearch_r', 'htonl', 'htons', 'hypot', 'hypotf', 'hypotl', 'iconv', 'iconv_close', 'iconv_open', 'IFTODT', 'if_freenameindex', 'if_indextoname', 'if_nameindex', 'if_nametoindex', 'ilogb', 'ilogbf', 'ilogbl', 'imaxabs', 'imaxdiv', 'index', 'inet_addr', 'inet_aton', 'inet_lnaof', 'inet_makeaddr', 'inet_netof', 'inet_network', 'inet_ntoa', 'inet_ntop', 'inet_pton', 'initgroups', 'initstate', 'initstate_r', 'innetgr', 'ioctl', 'isalnum', 'isalpha', 'isascii', 'isatty', 'isblank', 'iscntrl', 'isdigit', 'isfinite', 'isgraph', 'isgreater', 'isgreaterequal', 'isinf', 'isinff', 'isinfl', 'isless', 'islessequal', 'islessgreater', 'islower', 'isnan', 'isnan', 'isnanf', 'isnanl', 'isnormal', 'isprint', 'ispunct', 'issignaling', 'isspace', 'isunordered', 'isupper', 'iswalnum', 'iswalpha', 'iswblank', 'iswcntrl', 'iswctype', 'iswdigit', 'iswgraph', 'iswlower', 'iswprint', 'iswpunct', 'iswspace', 'iswupper', 'iswxdigit', 'isxdigit', 'j0', 'j0f', 'j0l', 'j1', 'j1f', 'j1l', 'jn', 'jnf', 'jnl', 'jrand48', 'jrand48_r', 'kill', 'killpg', 'l64a', 'labs', 'lcong48', 'lcong48_r', 'ldexp', 'ldexpf', 'ldexpl', 'ldiv', 'lfind', 'lgamma', 'lgammaf', 'lgammaf_r', 'lgammal', 'lgammal_r', 'lgamma_r', 'link', 'lio_listio', 'lio_listio64', 'listen', 'llabs', 'lldiv', 'llrint', 'llrintf', 'llrintl', 'llround', 'llroundf', 'llroundl', 'localeconv', 'localtime', 'localtime_r', 'log', 'log10', 'log10f', 'log10l', 'log1p', 'log1pf', 'log1pl', 'log2', 'log2f', 'log2l', 'logb', 'logbf', 'logbl', 'logf', 'login', 'login_tty', 'logl', 'logout', 'logwtmp', 'longjmp', 'lrand48', 'lrand48_r', 'lrint', 'lrintf', 'lrintl', 'lround', 'lroundf', 'lroundl', 'lsearch', 'lseek', 'lseek64', 'lstat', 'lstat64', 'lutimes', 'madvise', 'makecontext', 'mallinfo', 'malloc', 'mallopt', 'matherr', 'mblen', 'mbrlen', 'mbrtowc', 'mbsinit', 'mbsnrtowcs', 'mbsrtowcs', 'mbstowcs', 'mbtowc', 'mcheck', 'memalign', 'memccpy', 'memchr', 'memcmp', 'memcpy', 'memfrob', 'memmem', 'memmove', 'mempcpy', 'memrchr', 'memset', 'mkdir', 'mkdtemp', 'mkfifo', 'mknod', 'mkstemp', 'mktemp', 'mktime', 'mlock', 'mlockall', 'mmap', 'mmap64', 'modf', 'modff', 'modfl', 'mount', 'mprobe', 'mrand48', 'mrand48_r', 'mremap', 'msync', 'mtrace', 'munlock', 'munlockall', 'munmap', 'muntrace', 'nan', 'nanf', 'nanl', 'nanosleep', 'nearbyint', 'nearbyintf', 'nearbyintl', 'nextafter', 'nextafterf', 'nextafterl', 'nexttoward', 'nexttowardf', 'nexttowardl', 'nftw', 'nftw64', 'ngettext', 'nice', 'nl_langinfo', 'notfound', 'nrand48', 'nrand48_r', 'ntohl', 'ntohs', 'ntp_adjtime', 'ntp_gettime', 'obstack_1grow', 'obstack_1grow_fast', 'obstack_alignment_mask', 'obstack_alloc', 'obstack_base', 'obstack_blank', 'obstack_blank_fast', 'obstack_chunk_alloc', 'obstack_chunk_free', 'obstack_chunk_size', 'obstack_copy', 'obstack_copy0', 'obstack_finish', 'obstack_free', 'obstack_grow', 'obstack_grow0', 'obstack_init', 'obstack_int_grow', 'obstack_int_grow_fast', 'obstack_next_free', 'obstack_object_size', 'obstack_object_size', 'obstack_printf', 'obstack_ptr_grow', 'obstack_ptr_grow_fast', 'obstack_room', 'obstack_vprintf', 'offsetof', 'on_exit', 'open', 'open64', 'opendir', 'openlog', 'openpty', 'open_memstream', 'parse_printf_format', 'pathconf', 'pause', 'pclose', 'perror', 'pipe', 'popen', 'posix_memalign', 'pow', 'pow10', 'pow10f', 'pow10l', 'powf', 'powl', 'pread', 'pread64', 'printf', 'printf_size', 'printf_size_info', 'psignal', 'pthread_getattr_default_np', 'pthread_key_create', 'pthread_key_delete', 'pthread_setattr_default_np', 'pthread_setspecific', 'ptsname', 'ptsname_r', 'putc', 'putchar', 'putchar_unlocked', 'putc_unlocked', 'putenv', 'putpwent', 'puts', 'pututline', 'pututxline', 'putw', 'putwc', 'putwchar', 'putwchar_unlocked', 'putwc_unlocked', 'pwrite', 'pwrite64', 'qecvt', 'qecvt_r', 'qfcvt', 'qfcvt_r', 'qgcvt', 'qsort', 'raise', 'rand', 'random', 'random_r', 'rand_r', 'rawmemchr', 'read', 'readdir', 'readdir64', 'readdir64_r', 'readdir_r', 'readlink', 'readv', 'realloc', 'realpath', 'recv', 'recvfrom', 'regcomp', 'regerror', 'regexec', 'regfree', 'register_printf_function', 'remainder', 'remainderf', 'remainderl', 'remove', 'rename', 'rewind', 'rewinddir', 'rindex', 'rint', 'rintf', 'rintl', 'rmdir', 'round', 'roundf', 'roundl', 'rpmatch', 'scalb', 'scalbf', 'scalbl', 'scalbln', 'scalblnf', 'scalblnl', 'scalbn', 'scalbnf', 'scalbnl', 'scandir', 'scandir64', 'scanf', 'sched_getaffinity', 'sched_getparam', 'sched_getscheduler', 'sched_get_priority_max', 'sched_get_priority_min', 'sched_rr_get_interval', 'sched_setaffinity', 'sched_setparam', 'sched_setscheduler', 'sched_yield', 'secure_getenv', 'seed48', 'seed48_r', 'seekdir', 'select', 'semctl', 'semget', 'semop', 'semtimedop', 'sem_close', 'sem_destroy', 'sem_getvalue', 'sem_init', 'sem_post', 'sem_timedwait', 'sem_trywait', 'sem_unlink', 'sem_wait', 'send', 'sendto', 'setbuf', 'setbuffer', 'setcontext', 'setdomainname', 'setegid', 'setenv', 'seteuid', 'setfsent', 'setgid', 'setgrent', 'setgroups', 'sethostent', 'sethostid', 'sethostname', 'setitimer', 'setjmp', 'setkey', 'setkey_r', 'setlinebuf', 'setlocale', 'setlogmask', 'setmntent', 'setnetent', 'setnetgrent', 'setpgid', 'setpgrp', 'setpriority', 'setprotoent', 'setpwent', 'setregid', 'setreuid', 'setrlimit', 'setrlimit64', 'setservent', 'setsid', 'setsockopt', 'setstate', 'setstate_r', 'settimeofday', 'setuid', 'setutent', 'setutxent', 'setvbuf', 'shm_open', 'shm_unlink', 'shutdown', 'sigaction', 'sigaddset', 'sigaltstack', 'sigblock', 'sigdelset', 'sigemptyset', 'sigfillset', 'siginterrupt', 'sigismember', 'siglongjmp', 'sigmask', 'signal', 'signbit', 'significand', 'significandf', 'significandl', 'sigpause', 'sigpending', 'sigprocmask', 'sigsetjmp', 'sigsetmask', 'sigstack', 'sigsuspend', 'sigvec', 'sin', 'sincos', 'sincosf', 'sincosl', 'sinf', 'sinh', 'sinhf', 'sinhl', 'sinl', 'sleep', 'snprintf', 'socket', 'socketpair', 'sprintf', 'sqrt', 'sqrtf', 'sqrtl', 'srand', 'srand48', 'srand48_r', 'srandom', 'srandom_r', 'sscanf', 'ssignal', 'stat', 'stat64', 'stime', 'stpcpy', 'stpncpy', 'strcasecmp', 'strcasestr', 'strcat', 'strchr', 'strchrnul', 'strcmp', 'strcoll', 'strcpy', 'strcspn', 'strdup', 'strdupa', 'strerror', 'strerror_r', 'strfmon', 'strfry', 'strftime', 'strlen', 'strncasecmp', 'strncat', 'strncmp', 'strncpy', 'strndup', 'strndupa', 'strnlen', 'strpbrk', 'strptime', 'strrchr', 'strsep', 'strsignal', 'strspn', 'strstr', 'strtod', 'strtof', 'strtoimax', 'strtok', 'strtok_r', 'strtol', 'strtold', 'strtoll', 'strtoq', 'strtoul', 'strtoull', 'strtoumax', 'strtouq', 'strverscmp', 'strxfrm', 'stty', 'success', 'SUN_LEN', 'swapcontext', 'swprintf', 'swscanf', 'symlink', 'sync', 'syscall', 'sysconf', 'sysctl', 'syslog', 'system', 'sysv_signal', 'S_ISBLK', 'S_ISCHR', 'S_ISDIR', 'S_ISFIFO', 'S_ISLNK', 'S_ISREG', 'S_ISSOCK', 'S_TYPEISMQ', 'S_TYPEISSEM', 'S_TYPEISSHM', 'tan', 'tanf', 'tanh', 'tanhf', 'tanhl', 'tanl', 'tcdrain', 'tcflow', 'tcflush', 'tcgetattr', 'tcgetpgrp', 'tcgetsid', 'tcsendbreak', 'tcsetattr', 'tcsetpgrp', 'tdelete', 'tdestroy', 'telldir', 'tempnam', 'TEMP_FAILURE_RETRY', 'textdomain', 'tfind', 'tgamma', 'tgammaf', 'tgammal', 'time', 'timegm', 'timelocal', 'times', 'tmpfile', 'tmpfile64', 'tmpnam', 'tmpnam_r', 'toascii', 'tolower', 'toupper', 'towctrans', 'towlower', 'towupper', 'trunc', 'truncate', 'truncate64', 'truncf', 'truncl', 'tryagain', 'tsearch', 'ttyname', 'ttyname_r', 'twalk', 'tzset', 'ulimit', 'umask', 'umount', 'umount2', 'uname', 'unavail', 'ungetc', 'ungetwc', 'unlink', 'unlockpt', 'unsetenv', 'updwtmp', 'utime', 'utimes', 'utmpname', 'utmpxname', 'valloc', 'vasprintf', 'va_arg', 'va_copy', 'va_end', 'va_start', 'verr', 'verrx', 'versionsort', 'versionsort64', 'vfork', 'vfprintf', 'vfscanf', 'vfwprintf', 'vfwscanf', 'vlimit', 'vprintf', 'vscanf', 'vsnprintf', 'vsprintf', 'vsscanf', 'vswprintf', 'vswscanf', 'vsyslog', 'vtimes', 'vwarn', 'vwarnx', 'vwprintf', 'vwscanf', 'wait', 'wait3', 'wait4', 'waitpid', 'warn', 'warnx', 'WCOREDUMP', 'wcpcpy', 'wcpncpy', 'wcrtomb', 'wcscasecmp', 'wcscat', 'wcschr', 'wcschrnul', 'wcscmp', 'wcscoll', 'wcscpy', 'wcscspn', 'wcsdup', 'wcsftime', 'wcslen', 'wcsncasecmp', 'wcsncat', 'wcsncmp', 'wcsncpy', 'wcsnlen', 'wcsnrtombs', 'wcspbrk', 'wcsrchr', 'wcsrtombs', 'wcsspn', 'wcsstr', 'wcstod', 'wcstof', 'wcstoimax', 'wcstok', 'wcstol', 'wcstold', 'wcstoll', 'wcstombs', 'wcstoq', 'wcstoul', 'wcstoull', 'wcstoumax', 'wcstouq', 'wcswcs', 'wcsxfrm', 'wctob', 'wctomb', 'wctrans', 'wctype', 'WEXITSTATUS', 'WIFEXITED', 'WIFSIGNALED', 'WIFSTOPPED', 'wmemchr', 'wmemcmp', 'wmemcpy', 'wmemmove', 'wmempcpy', 'wmemset', 'wordexp', 'wordfree', 'wprintf', 'write', 'writev', 'wscanf', 'WSTOPSIG', 'WTERMSIG', 'y0', 'y0f', 'y0l', 'y1', 'y1f', 'y1l', 'yn', 'ynf', 'ynl']

    android_input_functions = ['onActivityResult',
                               'onCreate',
                               'onRestoreInstanceState',
                               'ContentResolver.query',
                               'onStartCommand',
                               'onBind']

    android_output_functions = ['startActivity',
                                'startActivityForResult',
                                'startService',
                                'bindService',
                                'sendBroadcast',
                                'sendOrderedBroadcast',
                                'sendStickyBroadcast',
                                'getSharedPreferences',
                                'openFileOutput',
                                'openOrCreateDatabase',
                                'ContentResolver.insert',
                                'ContentResolver.update',
                                'ContentResolver.delete',
                                'onSaveInstanceState',
                                'onCreateView']

    indent = "    "

    def __init__(self, name, signature, environment):
        """
            Call constructor.
        
            Receives a line of cflow's output and parses it for some key information such as indent level,
            function name, signature and the point where it's defined.

            Args:
                name: A String containing the name of the function this Call represents.
                signature: A piece of information associated with the function this Call represents. In the current
                    implementation it is the name of the file where the function is defined.
                
            Returns:
                A new instance of Call.
        """
        self._function_name = name
        self._function_signature = signature
        self._environment = environment

    @classmethod
    def from_cflow(cls, cflow_line):
        cflow_line_parser = CflowLineParser.get_instance(cflow_line)

        new_instance = cls(cflow_line_parser.get_function_name(),
                           cflow_line_parser.get_function_signature(),
                           Environments.C)
        new_instance.level = cflow_line_parser.get_level()

        return new_instance

    @classmethod
    def from_gprof(cls, gprof_line):
        gprof_line_parser = GprofLineParser.get_instance(gprof_line)

        new_instance = cls(gprof_line_parser.get_function_name(),
                           gprof_line_parser.get_function_signature(),
                           Environments.C)

        return new_instance

    @classmethod
    def from_javacg(cls, javacg_line):
        javacg_line_parser = JavaCGLineParser.get_instance(javacg_line)

        new_instance = cls(javacg_line_parser.get_function_name(),
                           javacg_line_parser.get_function_signature(),
                           Environments.ANDROID)

        new_instance.class_name = javacg_line_parser.get_class()
        new_instance.package_name = javacg_line_parser.get_package()

        return new_instance

    def __str__(self):
        """
            Returns a string representation of the Call.

            Returns:
                A String representation of the Call
        """
        if self._environment == Environments.ANDROID:
            return self.function_signature + "." + self.function_name
        else:
            return self.identity

    def __hash__(self):
        """
            Returns a number that uniquely identifies this instance.
                
            Returns:
                An Int that represents the calculated hash of this instance.
        """
        return hash(self.identity)

    def __eq__(self, other):
        """
            Overrides == operator. Compares this instance of Call with another instance for equality.

            Args:
                other: The other instance of Call to compare this instance to.

            Returns:
                A Boolean that says whether this instance can be considered equal to other.
        """
        # return hash(self) == hash(other)

        return self.identity == other.identity

    def __ne__(self, other):
        """
            Overrides != operator. Compares this instance of Call with another instance for inequality.

            Args:
                other: The other instance of Call to compare this instance to.

            Returns:
                A Boolean that says whether this instance can be considered not equal to other.
        """
        return self.identity != other.identity

    def is_input_function(self):
        """
            Determines whether the function represented by this object is an input function.

            Returns:
                A Boolean that states whether this object is an input function.
        """
        is_input = False

        if self._environment == Environments.C:
            is_input = self.function_name in Call.c_input_functions
        elif self._environment == Environments.ANDROID:
            is_input = (self.function_signature + "." + self.function_name) in Call.android_input_functions

        return is_input

    def is_output_function(self):
        """
            Determines whether the function represented by this object is an output function.

            Returns:
                A Boolean that states whether this object is an output function.
        """
        is_output = False

        if self._environment == Environments.C:
            is_output = self.function_name in Call.c_output_functions
        elif self._environment == Environments.ANDROID:
            is_output = (self.function_signature + "." + self.function_name) in Call.android_output_functions

        return is_output

    def is_standard_library_function(self):
        """
            Determines whether the function represented by this object is a standard library function.

            Returns:
                A Boolean that states whether this object is a standard library function.
        """
        return self.function_name in Call.c_standard_library_functions

    def is_function_name_only(self):
        return False if self._function_signature else True

    @property
    def identity(self):
        """
            Returns a string that uniquely identifies this object.

            Returns:
                A String that contains a unique representation of this object.
        """
        value = self.function_name

        if self.function_signature:
            value += ' ' + self.function_signature

        return value

    @property
    def function_name(self):
        """
            Returns the name of the function call represented by this Call.

            Returns:
                A String containing the name of the function call represented by this object.
        """
        return self._function_name

    @property
    def function_signature(self):
        """
            Returns the signature and file location of the function call represented by this object.

            Returns:
                A String containing the function signature and file location of the call represented by this object
        """
        # TODO: This should be renamed to something like file or file_location or file_name.
        return self._function_signature

    def set_function_signature(self, new_function_signature):
        """
            Sets the function_signature property.

        Args:
            new_function_signature: A string representing the new function signature to set.
        """
        self._function_signature = new_function_signature