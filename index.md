Programming Problem: ATM Protocol
=================================

Summary
-------

For this assignment, you will implement an
ATM communication protocol. There will be two programs.
One program, called `atm`, will allow bank customers to withdraw and
deposit money from their account.
The other program, called `bank`, will run as a server that keeps
track of customer balances.

Your ATM and bank code are due Monday December 2. You'll then
attack each others' 

You may work in a group of up to 2 (but you don't have to). I will take
into account whether you were in a group when I assess how ambitious
you were in your implementation.


Security Model
--------------

`atm` and `bank` must be implemented such that only a customer with a
correct _card file_ can learn or modify the balance of their account,
and only in an appropriate way (e.g., they may not withdraw more money
than they have).
In addition, an `atm` may only communicate with a `bank` if it and
the bank agree on an _auth file_, which they use to mutually
authenticate. 
The _auth file_ will be shared between the `bank` and `atm` via a 
trusted channel unavailable to the attacker, and is used to set up
secure communications.

You should approach this project with a "real world" attacker in mind,
but practically, your code will be attacked by 

Since the ATM client is communicating with the bank server over the
network, it is possible that there is a "man in the middle" that can
observe and change the messages, or insert new messages.
 A "man in the middle" attacker can view all traffic transmitted 
between the `atm` and the `bank`. 
The "man in the middle" may send messages to either the atm
or the bank. (You'll write code for this man-in-the-middle in our
last lab!)

The source code for `atm` and `bank` will be available to attackers,
but not the auth file. The card file may be available in some cases,
depending on the kind of attack.

Requirements
--------

Your implementation must be in Python 3. You may import packages
of your choice but *only with preapproval*. Packages must
be installable via homebrew or pip. (If you would like to use
a dependency manager like pipenv, come talk to me first.)

The specification details for each program are linked below.

- [Bank Server](bank.md)
- [ATM Client](atm.md)

Here are some general requirements that apply to both `atm` and `bank`
programs. (Throughout, "exit code" or "return code" refer interchangeably
to the integer provided by your program when it exits, which in Python
can be done with `sys.exit([code]])`.)

### Valid Inputs

Any command-line input that is not valid according to the rules below
should result with an exit code of 255 from the invoked program and
nothing should be output to ***stdout***.

- Command line arguments must be [POSIX
  compliant](http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)
  and each argument cannot exceed 4096 characters (with additional
  restrictions below).
  In particular, this allows command arguments specified
  as "-i 4000" to be provided without the space as "-i4000" or with
  extra spaces as in "-i &nbsp;&nbsp;&nbsp; 4000".
  Arguments may appear in any order. You should not implement `--`, 
  which is optional for POSIX compliance. You should implement guideline
  5 (ex. `atm -ga ray` is valid).

- Numeric inputs are positive and provided in decimal without any
 leading 0's (should match __/(0|[1-9][0-9]*)/__).
 Thus "42" is a valid input number but the octal "052" or hexadecimal
  "0x2a" are not.
 Any reference to "**number**" below refers to this input specification.
  
- Balances and currency amounts are specified as a **number** indicating a
  whole amount and a fractional input separated by a period.
  The fractional input is in decimal and is always two digits and thus
  *can include a leading 0* (should match **/[0-9]{2}/**).
 The interpretation of the fractional amount *v* is that of having
  value equal to *v*/100 of a whole amount (akin to cents and dollars
  in US currency). 
  Command line input amounts are bounded from 0.00 to 4294967295.99 inclusively but an account may accrue any non-negative balance over multiple transactions.
  
- File names are restricted to underscores, hyphens, dots, digits,
  and lowercase alphabetical characters (each character should match
  **/[_\\-\\.0-9a-z]/**).
  File names are to be between 1 and 127 characters long. The special
  file names "." and ".." are not allowed.
  
- Account names are restricted to same characters as file names but
  they are inclusively between 1 and 122 characters of length, and "." and ".." are
  valid account names. 

- IP addresses are restricted to IPv4 32-bit addresses and are
  provided on the command line in dotted decimal notation, i.e., four
  **numbers** between 0 and 255 separated by periods.

- Ports are specified as **numbers** between 1024 and 65535
  inclusively.

### Outputs

- Anything printed to **stderr** will be ignored (e.g., so detailed error
  messages could be printed there, if desired).
  
- All JSON output is printed on a single line and is followed by a newline.

- JSON outputs must show numbers (including potentially unbounded account balances) with full precision. 

- Newlines are '\n' -- the ASCII character with code decimal 10.

- Both programs should **explicitly flush stdout** after every line printed.

- Successful exits should return exit code 0.

### Errors

#### Protocol Error
  
- If an error is detected in the protocol's communication, `atm`
  should exit with return code `63`, while `bank` should print
  "`protocol_error`" to stdout (followed by a newline) and roll back
  (i.e., undo any changes made by) the current transaction.

- A timeout occurs if the other program does not respond within 10 seconds.
  If the atm observes the timeout, it should exit with return code
  `63`, while if the bank observes it, it should print
  "`protocol_error`" to stdout (followed by a newline) and rollback
  the current transaction.
  The non-observing party need not do anything in particular.

- If `atm` cannot connect to the bank, it should exit with return code `63`.

#### Other Errors

- All other errors, specified throughout this specification or
  unrecoverable errors not explicitly discussed, should prompt the
  program to exit with return code `255`.
  
Oracle
------

Soon (TM) you'll be provided an _oracle_ for a reference implementation.
This will be our "source of truth" for determining what is (or isn't)
a correctness bug. (Bugs in the oracle are discussed below.)

You will be able to query the oracle to clarify
the expected behavior of the `atm` and `bank` programs. Queries are
specified as a sequence of `atm` commands.
Here is an example query (this will make more sense if you read the
specifications for the `atm` and `bank` programs first):

	[ 
		{"input":["-p", "%PORT%", "-i", "%IP%", "-a", "ted", "-n", "10.30"],"base64":false}, 
		{"input":["-p", "%PORT%", "-i", "%IP%", "-a", "ted", "-d", "5.00"]}, 
		{"input":["-p", "%PORT%", "-i", "%IP%", "-a", "ted", "-g"]},
		{"input":["LXA=", "JVBPUlQl", "LWk=", "JUlQJQ==", "LWE=", "dGVk", "LWc="],"base64":true} 
	]

The oracle will provide outputs from the atm and bank. Here is an example for the previous query:

	[
		{
			"bank": {
				"output": {"initial_balance": 10.3,"account": "ted"}
			},
			"atm": {
				"exit": 0,
				"output": {"initial_balance": 10.3,"account": "ted"}
			}
		},
		{
			"bank": {
				"output": {"deposit": 5,"account": "ted"
				}
			},
			"atm": {
				"exit": 0,
				"output": {"deposit": 5,"account": "ted"}
			}
		},
		{
			"bank": {
				"output": {"balance": 15.3,"account": "ted"}
			},
			"atm": {
				"exit": 0,
				"output": {"balance": 15.3,"account": "ted"}
			}
		},
		{
			"bank": {
				"output": {"balance": 15.3,"account": "ted"}
			},
			"atm": {
				"exit": 0,
				"output": {"balance": 15.3,"account": "ted"}
			}
		}
	]

In general, a test must begin with account creation, so that the atm
program creates a card file, which can be used on subsequent
interactions. Though we have not shown it, you can also pass the
cardfile explicitly during a test, i.e., using the `-c` option.

The `bank` will run at a dynamically chosen IP address, listening on a
dynamically chosen port. Since this information cannot be known when
writing the query, you instead specify these values using the
following variables:

- `%IP%` - IP address of the `bank` server
- `%PORT%` - TCP port of the `bank` server

Each "input" is the argument list passed to `atm`. 
Queries may specify inputs using base64-encoded values by by providing
the optional boolean field `"base64"`. 


Changes and Oracle Updates
-------

There will inevitably be changes to the specification and oracle
implementation as unclear assumptions and mistakes are uncovered
on my end. Apologies in advance!

All changes will be posted on the Moodle page under 'P4 Updates'.

If there are bugs in the reference implementation (and there probably
will be), a small amount of bonus points will be awarded to the first group
to report each bug.

Submission
-------------------------

Each group should create a git repository on [github](https://github.com/).
Create a directory named `build` in the top-level directory of this repository
and commit your code into that folder. (Gradescope allows you to submit
via github!)

When I run tests, I will first `cd` into the `build` directory.

Once make finishes, `atm` and `bank` should be executable 
files within the `build` directory. An automated system will invoke `atm.py`
and `bank.py` with a variety of options and measure their responses. 
Your programs must be able to be run from any working directory
(in other words, your programs shouldn't hardcode specific directory or path names),
but I'll preserve your directory structure along with any helper files.


Examples
--------

Here is an example of how to use `atm` and `bank`. 
First, do some setup and run `bank`.

	$ mkdir bankdir; mv bank bankdir/; cd bankdir/; ./bank -s bank.auth &; cd ..
	created

Now set up the atm. 

	$ mkdir atmdir; cp bankdir/bank.auth atmdir/; mv atm atmdir/; cd atmdir

Create an account 'bob' with balance $1000.00 (There are two outputs because one is from the `bank` which is running in the same shell).

	$ ./atm -s bank.auth -c bob.card -a bob -n 1000.00
	{"account":"bob","initial_balance":1000}
	{"account":"bob","initial_balance":1000}

Deposit $100.

	$ ./atm -c bob.card -a bob -d 100.00
	{"account":"bob","deposit":100}
	{"account":"bob","deposit":100}

Withdraw $63.10.

	$ ./atm -c bob.card -a bob -w 63.10
	{"account":"bob","withdraw":63.1}
	{"account":"bob","withdraw":63.1}

Attempt to withdraw $2000, which fails since 'bob' does not have a sufficient balance.

	$ ./atm -c bob.card -a bob -w 2000.00
	$ echo $?
	255

Attempt to create another account 'bob', which fails since the account 'bob' already exists.

	$ ./atm -a bob -n 2000.00
	$ echo $?
	255

Create an account 'alice' with balance $1500.

	$ ./atm -a alice -n 1500.00
	{"account":"alice","initial_balance":1500}
	{"account":"alice","initial_balance":1500}

Bob attempts to access alice's balance with his card, which fails.

	$ ./atm -a alice -c bob.card -g
	$ echo $?
	255

 A note on concurrent transactions 
 ---------------------------------

In principle, the bank could accept transaction requests from multiple ATMs concurrently, if it chose to---there is no requirement that it must. 
If it does, the order that these transactions take effect is non-deterministic, but atomic. 
For example, if ATM 1 requested a deposit of \$50 to Bob's account
and ATM 2 requested a withdrawal of \$25 from Bob's account, those two requests could take effect in either order, but when they complete Bob should always be $25 richer. 
Note that an atomic transaction includes both changes/accesses to the balance and the corresponding I/O. 
As such, the order of any printed statements about events must match the order the events actually took place.

My testing won't test concurrent transactions. Tests are sequences of synchronous ATM commands. During the break-it lab, tests also involve a "man in the middle" (MITM) which could introduce concurrency (see the description of the attacker model), but the MITM will never have direct access to the card file or auth file, so its ability to initiate concurrent transactions is more limited than the ATM.