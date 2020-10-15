#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define SUM 20              //种群数目
#define MAXloop 400           //最大循环次数
#define error 0.00001       //若两次最优值之差小于此数则认为结果没有改变
#define crossp 0.7            //交叉概率
#define mp 0.04               //变异概率
#define TestFunction x*(x*(x*(x*(x*(x-10)-26)+344)+193)-1846)-1680


//用于求解函数y=x^6-10x^5-26x^4+344x^3+193x^2-1846x-1680在（-8，8）之间的最小值
 
typedef struct              //定义染色体结构
{
    int info;                //染色体结构，用一整型数的后14位作为染色体编码
    double suitability;        //次染色体所对应的适应度函数值，在本题中为表达式的值
} gen;
gen gen_group[SUM];            //定义父种群
gen gen_new[SUM];          //定义交叉产生的子种群
 
gen gen_result;                //记录最优的染色体
int result_unchange_time;     //记录在error前提下最优值为改变的循环次数
 
 
/**************函数声明******************/
/***********主函数调用函数***************/
void  initiate();              //初始化函数，主要负责产生初始化种群
void  evaluation();            //评估种群中各染色体的适应度，并据此进行排序
int   record();                //记录每次循环产生的最优解并判断是否终止循环
void  cross();                //交叉函数
void  mutation();            //变异函数
void  selection();            //选择函数
gen   showresult(int);        //显示结果
 
/**************其他函数******************/
int    randsign(double p);              //按照概率p产生随机数0、1，其值为1的概率为p
int    randbit(int i,int j);        //产生一个在i，j两个数之间的随机整数
int    randnum();                    //随机产生一个由14个基因组成的染色体
int    convertionD2B(double x);        //对现实解空间的可能解x进行二进制编码（染色体形式）
double convertionB2D(int x);        //将二进制编码x转化为现实解空间的值
int    createmask(int a);            //用于交叉操作
void   QuickSort(gen* a, int low, int high);    //排序算法
 
int main()
{
    int i, run_time = 0;
    gen temp, z;
    temp.suitability = 1000;
    z.suitability = 1000;
    srand((unsigned)time(NULL));

    for(i = 0; i < 10; i++)
    {
        int i , flag = 0;
    
        initiate();                //产生初始化种群
        for( i = 0 ; i < MAXloop ; i++ )
        {
            evaluation();    //对种群进行评估、排序
            if( record() == 1 )    //满足终止规则1，则flag=1并停止循环
            {
                flag = 1;
                break;
            }
            
            cross();            //进行交叉操作
            mutation();            //变异操作
            selection();        //对父子种群中选择最优的NUM个作为新的父种群
            run_time++;
        }
        z = showresult( flag );    //按照flag显示寻优结果
        if(temp.suitability > z.suitability)
            temp = z;
    }

    printf("当取值x = %f时, 表达式y=x^6-10x^5-26x^4+344x^3+193x^2-1846x-1680达到最小值:\ny = %f\n",convertionB2D(temp.info), temp.suitability);

    system("pause");
    
    return 0;
}
 
void initiate()
{
    int i;
    for( i = 0 ; i < SUM ; i++ )
    {
        double x;
        gen_group[i].info = randnum();        //调用randnum()函数建立初始种群
        x = convertionB2D(gen_group[i].info);
        gen_group[i].suitability = TestFunction;     //提取公因式比原式更快
    }
        
    gen_result.suitability = 1000;
    result_unchange_time = 0;
}
 
void evaluation()
{
    QuickSort(gen_group, 0, SUM);
}

int record()    //记录最优解和判断是否满足条件
{
    double x;
 
    x = gen_result.suitability - gen_group[0].suitability;
    if(x < 0)x = -x;
    if(x < error)
    {
        result_unchange_time++;
        if(result_unchange_time >= 20)return 1;
    }
    else
    {
        gen_result.info = gen_group[0].info;
        gen_result.suitability = gen_group[0].suitability;
        result_unchange_time = 0;
    }
    
    return 0;
}
 
void cross()
{
    int i , j;
    int mask1 , mask2;

    for(i = 0 ; i < SUM ; i++)
    {
        double x = 0;
           j = randbit(i + 1 , SUM - 1);
        if(randsign(crossp) == 1)        //按照crossp的概率对选择的染色体进行交叉操作
        {
            mask1 = createmask(randbit(0 , 14));        //由ranbit选择交叉位
            mask2 = ~mask1;                //形成一个类似000111之类的二进制码编码
            gen_new[i].info = ((gen_group[i].info) & mask2) + ((gen_group[j].info) & mask1);
            x = convertionB2D(gen_new[i].info);
            gen_new[i].suitability = TestFunction;
        }
        else         //不进行交叉
        {
            gen_new[i].info = gen_group[i].info;
            gen_new[i].suitability = gen_group[i].suitability;
        }
    }
}

void mutation()
{
    int i, j;
    int gentinfo;
    double gentsuitability;
    for(i = 0 ; i < SUM ; i++)
    {
        if(randsign(mp) == 1)                    //按照变异概率进行变异操作
        {
            double x;
            int i , j = randbit(0 , 14);        //确定变异多少位
            for(i = 0 ; i < j ; i++)
            {
                int m , j = randbit(0 , 14);    //确定变异第几位
                m = 1 << j;
                gen_group[i].info = gen_group[i].info ^ m;
            }
            x = convertionB2D(gen_group[i].info);
            gen_group[i].suitability = TestFunction;
        }
    }
}
 
 
void selection()
{
    int i;
    
    QuickSort(gen_group, 0, SUM);
    QuickSort(gen_new, 0, SUM);
    for(i = 0; i < SUM; i++)
    {
        if(gen_group[i].suitability > gen_new[i].suitability)
        {
            gen_group[i].info = gen_new[i].info;
            gen_group[i].suitability = gen_new[i].suitability;
        }
    }
}
 
gen showresult(int flag)//显示搜索结果
{
    FILE* datafd;
    if((datafd = fopen("data.txt" , "a+")) == NULL)
    {
        printf("Cannot create/open file");
        exit(1);
    }
    
    if(flag == 0)
        fprintf(datafd, "已到最大搜索次数，搜索失败!");
    else
    {
        fprintf(datafd, "当取值x = %f时, 表达式y=x^6-10x^5-26x^4+344x^3+193x^2-1846x-1680达到最小值:\ny = %f\n",convertionB2D(gen_result.info),gen_result.suitability);
    }
    
    return gen_result;
}
 
int randsign(double p)//按概率p返回1
{
    if(rand() > (p * (RAND_MAX + 1)))
        return 0;
    else return 1;
}

int randbit(int i, int j)//产生在i与j之间的一个随机数
{
    int a , l;
    l = j - i + 1;
    a = i + rand() * l / (RAND_MAX + 1);
    return a;
}
int randnum()
{
    int x;
    x = (double)rand() / (RAND_MAX + 1) * 16000;
    return x;
}
double convertionB2D(int x)
{
    double y;
    y = x;
    y = (y - 8000) / 1000;
    return y;
    
}
int convertionD2B(double x)
{
    int g;
    g = (x * 1000) + 8000;
    return g;
}
int createmask(int a)
{
    int mask;
    mask=(1 << (a + 1)) - 1;
    return mask;
}

void QuickSort(gen* a, int low, int high)
{
     int i = low, j = high - 1;
    gen temp = a[low];  //取第一个元素为标准数据元素
    while(i < j)
    {
        while((i < j) && (temp.suitability <= a[j].suitability))
            j--; //在数组的右端扫描
        if(i < j)
        {
            a[i].info = a[j].info;
            a[i].suitability = a[j].suitability;
            i++;
        }
        while((i < j) && (a[i].suitability < temp.suitability))
            i++; //在数组的左端扫描
        if(i < j)
        {
            a[j].info = a[i].info;
            a[j].suitability = a[i].suitability;
            j--;
        }
    }
    a[i] = temp;
    if(low < i) QuickSort(a, low, i-1); //对左端子集合进行递归
    if(i < high) QuickSort(a, j+1, high);  //对右端子集合进行递归
}
