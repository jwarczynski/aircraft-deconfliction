# aircraft-deconfliction

This notebook solves create and solves linaer programming problem related to aircraft deconflictation.
Each plane has 7 possible maneuvers. The aim is to assign each plane such amaneuver that it is no conflicts.
In each input file ther is collison matrix in form

| \ | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| - | ------------------- | ------------------- | --- | ------------------- | ------------------- | --- | ------------------- |
| plane_1 maneouver_1 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| plane_1 maneouver_2 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| ... | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| plane_1 maneouver_7 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| plane_2 maneouver_1 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| ... | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 |
| plane_n maneouver_7 | plane_1 maneouver_1 | plane_1 maneouver_2 | ... | plane_1 maneouver_7 | plane_2 maneouver_1 | ... | plane_n maneouver_7 | 
