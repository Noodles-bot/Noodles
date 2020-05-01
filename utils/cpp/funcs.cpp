
#include <iostream>
#include <iomanip>
#include<string>
#define _USE_MATH_DEFINES
#include<math.h>
using namespace std;


void input(double& real, double& imag);
void output(double real, double imag);
double mag(double real, double imag);
void add(double &a, double &b, double c, double d);
void sub(double &a, double &b, double c, double d);
void multi(double &a, double &b, double c, double d);
bool div(double &a, double &b, double c, double d);

int main(void)
{
	char choice;
	double a, b, c, d;
	do
	{
		cout << "Option?(C, L, S, +, -, *, /): ";
		cin >> choice;
		if (choice == 'C')
		{
			input(a, b);
			output(a, b);
		}
		else if (choice == 'L')
		{
			cout << "Length current Value is " << fixed << setprecision(2) << mag(a, b) << endl;
		}
		else if (choice == '+')
		{
			input(c, d);
			add(a, b, c, d);
		}
		else if (choice == '-')
		{
			input(c, d);
			sub(a, b, c, d);
		}
		else if (choice == '*')
		{
			input(c, d);
			multi(a, b, c, d);
		}
		else if (choice == '/')
		{
			input(c, d);
			if (!div(a, b, c, d))
				cout << "Illegal attempt to divide by 0 " << endl;
		}



	} while (choice != 'S');


	return 0;
}
void input(double& real, double& imag)
{
	cout << "Please input real part: ";
	cin >> real;
	cout << "Please input imag part: ";
	cin >> imag;
}
void output(double real, double imag)
{
	cout << fixed << setprecision(2) << "Current value is " << real << " + " << imag << "i" << endl;
}
double mag(double real, double imag)
{
	return sqrt((real*real) + (imag*imag));
}
void add(double &a, double &b, double c, double d)
{
	a = (a + c);
	b = (b + d);
	output(a, b);
}
void sub(double &a, double &b, double c, double d)
{
	a = (a - c);
	b = (b - d);
	output(a, b);
}
void multi(double &a, double &b, double c, double d)
{
	a = (a*c) - (b*d);
	b = (a*d) + (b*c);
	output(a, b);
}
bool div(double &a, double &b, double c, double d)
{
	if (c == 0 && d == 0)
		return false;

	a = (a*c) - (b*d) / (c*c) + (d*d);
	b = (a*d) + (b*c) / (c*c) + (d*d);
	output(a, b);
	return true;


}
