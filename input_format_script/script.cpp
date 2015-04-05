#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

using namespace std;


struct point
{
    int x,y;
};

int square(int num)
{
    return num*num;
}

int dist(struct point a,struct point b)
{
    return (int(sqrt(square(a.x- b.x) + square(a.y - b.y)))/100)*4;
}

int main(void)
{
    fstream edges, idb, write_file;
    edges.open("edges.txt");
    idb.open("idb-location.txt");
    write_file.open("input_20.txt", fstream::out);

    vector<point> idb_point;

    point each_point;

    int number_points;

    idb >> number_points;

    for(int i=0; i < number_points; i++ )
    {
        point p;
        idb>>p.x>>p.y;
        idb_point.push_back(p);
    }

    vector<point> edge_set;

    point edge;

    while(edges>>edge.x>>edge.y)
    {
        edge_set.push_back(edge);
    }

    for(int i=0; i< number_points; i++)
        cout<< idb_point[i].x<<" "<<idb_point[i].y<<endl;

    cout<<"============="<<endl;

    for(int i=0; i< edge_set.size(); i++)
        cout<<edge_set[i].x<<" "<<edge_set[i].y<<endl;


    int matrix[number_points][number_points];

    for(int i=0; i< number_points; i++)
        for(int j=0; j< number_points; j++)
            matrix[i][j]=0;

        for(int i=0; i< edge_set.size(); i++)
        {
            int x= edge_set[i].x;
            int y= edge_set[i].y;
 //           int d=0;
//            cout<<"x,y: "<<x<<","<<y<<endl;
            int d= dist(idb_point[x],idb_point[y]);
            matrix[x][y]= d;
            matrix[y][x]= d;
        }

        // cout<<idb_point[0].x<<" "<<idb_point[1].x<<endl;
        // point a= idb_point[0];
        // point b= idb_point[1];
        // int d= distance(a,b);
        // cout<<"===> "<<d<<endl;

        for(int i=0; i< number_points; i++)
        {
            for(int j=0; j< number_points; j++)
            {
                cout<<matrix[i][j]<<" ";
                write_file<<matrix[i][j]<<" ";
            }
            write_file<<"\n";
            cout<<endl;
        }
        write_file.close();

    }