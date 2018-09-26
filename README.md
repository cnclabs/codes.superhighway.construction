# Superhighway
A network construction solution for item-shared cross-domain recommendation.
# Usage
```txt
usage: superhighway.py [-h] [--source_data [SOURCE_DATA]]
                       [--target_data [TARGET_DATA]] [--alpha ALPHA]
                       [--beta BETA] [--output [OUTPUT]]

Superhighway Construction.

optional arguments:
  -h, --help            show this help message and exit
  --source_data [SOURCE_DATA]
                        Input source domain data
  --target_data [TARGET_DATA]
                        Input Target domain data
  --alpha ALPHA         Parameter for filtering user by the ratio of
                        overlapped items in each user's accessed item list
  --beta BETA           Parameter for setting the weight of superhighway
  --output [OUTPUT]
```

# Task
Given two network input:
```txt
src.txt:
userA itemA 3
userA itemC 5
userB itemA 1
userB itemB 5
userC itemA 4

tar.txt:
userD itemA 3
userE itemC 5
userF itemA 1
userF itemB 5
userG itemA 4

```

```txt
The proposed solution will build superhighways between users from two domains, respectlively:

userA userD 2 
userA userE 1  
.
.
.
```
