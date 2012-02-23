;;;
;;; This keyboard macro is for going through the code to where "ISSUE" is marked in the comments, grabbing the issue,
;;; putting it in a text file and then naming the function / class where the issue occurs. 
;;; It functions as a sort of easy to-do list generator for this project, so one can see the context of everything that
;;; remains to be done.
;;;
;;; It might be useful to convert this to emacs lisp in the future. But a keyboard macro is a rough and ready way of doing it.
;;;

;;; Goes through the document, finds issues in comments, defined by 'ISSUE' and then cuts untill next '.' then saves in a file called 'issues.txt' and lists the name of the function / class the comment was directly under. 
(fset 'enumerate\ issues
   "\C-sISSUE\C-[z.\C-y\C-x\C-fissues.txt\C-m\C-y\C-xb\C-m\C-[xre search backward\C-mclass \\| def\C-?\C-?\C-?\C-?def\C-m\C-k\C-y\C-xb\C-m\C-[a\C-y\C-m\C-[e\C-m\C-m\C-xb\C-m\C-[e")

