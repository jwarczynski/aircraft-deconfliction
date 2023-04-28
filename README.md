# aircraft-deconfliction

This notebook solves create and solves linear programming problem related to aircraft deconflictation.
Each plane has 7 possible maneuvers. The aim is to assign each plane such a maneuver that there is no conflicts between any two planes.
In each input file there is collison matrix in the following form:

| \ | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| - | ------------------- | ------------------- | --- | ------------------- | ------------------- | --- | ------------------- |
| plane_1 maneouver_1 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| plane_1 maneouver_2 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| ... | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| plane_1 maneouver_7 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| plane_2 maneouver_1 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| ... | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| plane_n maneouver_7 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 | 
