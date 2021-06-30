# Self Adaptive Ecosystem

Purpose of this project is create an automated home system which - 
1) Collects energy consumption of various electrical appliances of the house using ACS712 sensors attached to Nodemcu
2) Transmits this data to Raspberry PI using MQTT Protocol
3) Uses this data for analysis and create some graphs for easy visualisation by user
4) Utilises this data as dataset for predicting usage of appliances using LSTM Neural Network
5) Using predictions (binary output) and hardware 'Relays' to automate their usage without user intervention (Yet to be completed)


Graph of predicted vs actual values - 

<img src=https://github.com/shreyb99/self-adaptive-ecosystem/blob/main/pictures/graph.jpeg>
