To add a device you go into the devices.db and ad a device with a link to that devices .db file

In the devices db file add a list of questions In the DataQuestions table. 
	If the questions ask for data used by a technician in the Pos column add the word data,
	If the question has an answer link it to the answers table with a specific key, like 0
	If the answer will be given to the user when they answer yes, put a 1 in the ResAns column
	If the answer will be given to the user when they answer no, put a 0 in the ResAns clumn
In the devices Answers table link the answer with the key used befor in the pos coumn, and the answer in the Answer column