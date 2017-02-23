/*
	Implementation of a 'stat' command
	using the 'stat' system call and relevant masks
*/
// Unix systems programming

#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
	char *fd = argv[1];
	struct stat *buf;

	buf = malloc(sizeof(struct stat));

	stat(fd, buf);

	 switch (buf->st_mode & S_IFMT) {
           case S_IFBLK:  printf("\nType: block device");            break;
           case S_IFCHR:  printf("Type: character device");        break;
           case S_IFDIR:  printf("Type: directory");               break;
           case S_IFIFO:  printf("Type: FIFO/pipe");               break;
           case S_IFLNK:  printf("Type: symlink");                 break;
           case S_IFREG:  printf("Type: regular file");            break;
           case S_IFSOCK: printf("Type: socket");                  break;
           default:       printf("Type: unknown?");                break;
           }

	
	//printf("st_dev: %d", buf->st_dev);
	printf("\ninode no.: %d", buf->st_ino); 
	printf("\nMode: %d", buf->st_mode);
	printf("\nHard Links: %d", buf->st_nlink);
	printf("\nUserID of owner: %d", buf->st_uid);
	printf("\nGroupID of owner: %d", buf->st_gid);  	   
	printf("\nSize in bytes: %d", buf->st_size);
	printf("\nBlock size: %d", buf->st_blksize);
	printf("\nNo. of 512b blocks allocated: %d", buf->st_blocks);
	printf("\nTime of last access: %d", buf->st_atime);
	printf("\nTime of last modification: %d", buf->st_mtime);
	printf("\nTime of last status change: %d\n", buf->st_ctime);

	free(buf);
	return 0;
}


