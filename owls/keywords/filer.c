#include<stdio.h>
#include<stdlib.h>
int main()
{
    FILE *fp[8];
    char buf[1000],*pch,*out,flag;
    int num;
    fp[0]=fopen("final_output.txt","r");
    fp[1]=fopen("Economy.txt","a");
    fp[2]=fopen("Communication.txt","a");
    fp[3]=fopen("Education.txt","a");
    fp[4]=fopen("Food.txt","a");
    fp[5]=fopen("Weapon.txt","a");
    fp[6]=fopen("Medical.txt","a");
    fp[7]=fopen("Travel.txt","a");
    while (fgets(buf,1000,fp[0])!=NULL)
    {
        flag=0;
        pch = strtok(buf," ");
        while (pch != NULL)
        {
            if(!flag)
            {
                out=pch;
                flag=1;
            }
            else
            {
                num=atoi(pch);
                if(num)
                {
                    fprintf(fp[num],"%s\n",out);

                }
            }
            pch = strtok (NULL, " ");
        }
    }

    return 0;
}
