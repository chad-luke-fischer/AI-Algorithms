#include <iostream>
#include <fstream>
#include <cstring>
#include <vector>
#include <utility>
#include <algorithm>
#include <sstream>
#include <queue>
using namespace std;

//node struct for a star search
class node
{
   public:
      node(vector<vector<int> > _board,int _row,vector<pair<int,int> > _drones,int _in_hand);  // This is the constructor
      vector<vector<int> > board;
      int row;
      vector<pair<int,int> > drones;
      int in_hand;
   // private:
   //    vector<vector<int> > board;
   //    int row;
   //    vector<pair<int,int> > drones;
   //    int in_hand;
};

//  constructor
node::node(vector<vector<int> > _board,int _row,vector<pair<int,int> > _drones,int _in_hand)
{
   this->board = _board;
   this->row = _row;
   this->drones = _drones;
   this->in_hand = _in_hand;
}


bool isSafe(vector<vector<int> > board, int r, int c)
{
    // false if two queens share column
    for (int i = 0; i < r; i++)
        if (board[i][c] == 1)
            return false;
    // false if two queens share diagonal
    for (int i = r, j = c; i >= 0 && j >= 0; i--, j--)
        if (board[i][j] == 1)
            return false;
    // false if two queens share diagonal
    for (int i = r, j = c; i >= 0 && j < board.size(); i--, j++)
        if (board[i][j] == 1)
            return false;
    return true;
}

int check_score(vector<std::pair<int,int> > drones,vector<std::pair<int,int> > packs)
{
  int count = 0;
  for(int i = 0; i < drones.size();i++)
  {
    for(int j = 0; j < packs.size();j++)
    {
      if(drones[i]==packs[j])++count;
    }
  }
  return count;
}

int dfs(vector<vector<int> > board,int r,vector<std::pair<int,int> > drones,
            vector<std::pair<int,int> > packs,int total_drones,int max)
{
    if(drones.size()==total_drones)
    {
      if(check_score(drones, packs) > max)max=check_score(drones, packs);
      return max;
    }
    else if(r==board.size())return max;
    // place Queen at every square in current row r
    // and recur for each valid movement
    for (int i = 0; i < board.size(); i++)
    {
        // if no two queens threaten each other
        if (isSafe(board, r, i))
        {
            // place queen on current square
            board[r][i] = 1;

            drones.push_back(std::make_pair(r,i));
            max = dfs(board,r+1,drones,packs,total_drones,max);
            // backtrack and remove queen from current square
            board[r][i] = 0;
            drones.pop_back();
            if(i == board.size()-1 && total_drones - drones.size() < board.size()-r)
            {
              max = dfs(board,r+1,drones,packs,total_drones,max);
            }
        }
    }
    return max;
}
int a_star(vector<vector<int> > board,int r,vector<std::pair<int,int> > drones,
            vector<std::pair<int,int> > packs,int total_drones,int max)
{
node* _node = new node(board,r,packs, total_drones-drones.size());
priority_queue<int> frontier;
vector<node*> explored;
while (!frontier.empty())
{
  _node = frontier.top();
  if(_node->board.size()==total_drones)
  {
    if(score(_node->drones,_node->packs) > max)max=score(_node->drones,_node->packs);
    return max;
  }
  else if(_node->row==board.size())continue;
  explored.push_back(_node);
  for (int i = 0; i < _node->board.size(); i++)
  {
      if (isSafe(_node->board, _node->r, _node->i))
      {
          _node->board[r][i] = 1;
          _node->drones.push_back(std::make_pair(_node->row,i));
          max = a_star(_node->board,_node->row+1,_node->drones,packs,total_drones,max);
          _node->board[r][i] = 0;
          _node->drones.pop_back();
          int temp = node->in_hand;
          //node->in_hand = possible
          if(!explored.find(explored.begin(),explored.end(),_node))
          {
            frontier.push(node* node = new node(board,r+1,packs, total_drones-drones.size());//wrong
          }

          if(i == _node->board.size()-1 && total_drones - _node->drones.size() < _node->board.size()-_node->row)
          {
            max = a_star(_node->board,r+1,_node->drones,packs,total_drones,max);
          }
      }
  }

}


// int x;
// while (cin >> x) pq.push(x);
 while (not pq.empty()) {
// cout << pq.top() << endl;
// pq.pop();
//    return 0;
}
int main()
{
  std::ifstream file("input.txt");
  string n,initdrones,initpacks;
  string alg;
  std::getline(file,n);
  std::getline(file,initdrones);
  std::getline(file,initpacks);
  std::getline(file,alg);
  string cline;
  vector<std::pair<int,int> > drones;
  vector<std::pair<int,int> > packs;
  int _initdrones = std::stoi (initdrones);
  int _n = std::stoi (n);

  while (getline(file, cline ))
  {
    stringstream ss(cline);
    vector<int> temp;
    while(getline(ss, cline, ','))
    {
      temp.push_back(stoi(cline));
    }
    packs.push_back(std::make_pair(temp[0], temp[1]));
  }

    vector<vector<int> > board;
    vector<int> line;
    for(int i = 0; i < _n;i++)
    {
      for(int j = 0;j<_n;j++)
      {
        line.push_back(0);
      }
      board.push_back(line);
    }

    int res = a_star(board, 0,drones,packs,_initdrones,0);
    ofstream out;
    out.open ("output.txt");
    out << res;
    out.close();

    return 0;
}
