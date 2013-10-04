(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(column-number-mode t)
 '(show-paren-mode t)
 '(uniquify-buffer-name-style (quote forward) nil (uniquify)))

;;;
;;; Manually edited
;;;


;;
;; Add paths to 3rd party tools
;;
(add-to-list 'load-path "/home/ptracton/.emacs.d/third-party/")
;(add-to-list 'load-path "/home/ptracton/.emacs.d/third-party/predictive")
(add-to-list 'load-path "/home/ptracton/.emacs.d/third-party/color-theme-6.6.0")

(setq inhibit-startup-message t)        ; Do without annoying startup msg.

;;
;; http://www.emacswiki.org/emacs/PredictiveMode
;;
;(require 'predictive)
;(autoload 'predictive-mode "predictive" "predictive" t)
;(set-default 'predictive-auto-add-to-dict t)
;(setq 
;      predictive-auto-learn t
;      predictive-add-to-dict-ask nil
;      predictive-use-auto-learn-cache nil
;      predictive-which-dict t)


;;
;; Put the scroll bar on the right side
;; http://www.emacswiki.org/emacs/ScrollBar
;;
(set-scroll-bar-mode 'right) 

(require 'color-theme)
(color-theme-initialize)
(color-theme-clarity)
(setq my-color-themes (list 'color-theme-arjen 'color-theme-clarity
                              'color-theme-hober 'color-theme-billw
			      'color-theme-lethe 'color-theme-ld-dark
                              'color-theme-charcoal-black 'color-theme-late-night
                              'color-theme-midnight 'color-theme-tty-dark))
  (defun my-theme-set-default () ; Set the first row
      (interactive)
      (setq theme-current my-color-themes)
      (funcall (car theme-current)))
     
    (defun my-describe-theme () ; Show the current theme
      (interactive)
      (message "%s" (car theme-current)))
     
   ; Set the next theme (fixed by Chris Webber - tanks)
    (defun my-theme-cycle ()		
      (interactive)
      (setq theme-current (cdr theme-current))
      (if (null theme-current)
      (setq theme-current my-color-themes))
      (funcall (car theme-current))
      (message "%S" (car theme-current)))
    
    (setq theme-current my-color-themes)
    (setq color-theme-is-global nil) ; Initialization
    (my-theme-set-default)
    (global-set-key [f12] 'my-theme-cycle)

;;
;; http://www.emacswiki.org/emacs/NoTabs
;;
(setq indent-tabs-mode nil) 

;;
;; http://www.emacswiki.org/emacs/CProgrammingLanguage
;;
(setq c-default-style "python")
(setq-default c-basic-offset 4)
;	      c-indent-tabs-mode t 
;	      tab-width 4
;	      indent-tabs-mode t)
(add-hook 'c-mode-common-hook '(lambda () (c-toggle-auto-state 1)))

;;
;; Paren highlighting
;; http://www.emacswiki.org/emacs/HighlightParentheses
;;
;(add-hook 'highlight-parentheses-mode-hook
;          '(lambda ()
;             (setq autopair-handle-action-fns
;                   (append
;					(if autopair-handle-action-fns
;						autopair-handle-action-fns
;					  '(autopair-default-handle-action))
;					'((lambda (action pair pos-before)
;						(hl-paren-color-update)))))))
;
;(define-globalized-minor-mode global-highlight-parentheses-mode
;  highlight-parentheses-mode
;  (lambda ()
;    (highlight-parentheses-mode t)))
;(global-highlight-parentheses-mode t)


;;
;; Recentf is a minor mode that builds a list of recently opened files. This list is is automatically saved across Emacs sessions. You can then access this list through a menu.
;; http://www.emacswiki.org/emacs/RecentFiles
;;
(require 'recentf)
(recentf-mode 1)
(setq recentf-max-menu-items 25)
(global-set-key "\C-x\ \C-r" 'recentf-open-files)

;;
;; http://www.emacswiki.org/emacs/FrameTitle
;;
 (setq frame-title-format
          '(buffer-file-name
            "%f"
            (dired-directory dired-directory "%b")))


(setq ‘next-line-add-newlines’ 't)

;;
;; Verilog mode customization
;; http://www.cs.washington.edu/education/courses/cse467/04wi/misc/verilog-mode.el
;;
(setq verilog-indent-level             4
	  verilog-indent-level-module      4
	  verilog-indent-level-declaration 4
	  verilog-indent-level-behavioral  4
	  verilog-indent-level-directive   4
	  verilog-case-indent              2
	  verilog-auto-newline             t
	  verilog-auto-indent-on-newline   t
;	  verilog-tab-always-indent        t
	  verilog-auto-endcomments         t
      verilog-minimum-comment-distance 40
	  verilog-indent-begin-after-if    t
	  verilog-auto-lineup              '(all))

;;
;; http://www.veripool.org/projects/verilog-mode/wiki/Faq#Why-when-others-edit-my-code-does-it-looks-unindented
;;
(add-hook 'verilog-mode-hook '(lambda ()
    (add-hook 'local-write-file-hooks (lambda()
       (untabify (point-min) (point-max))))))

(add-hook 'verilog-mode-hook '(lambda ()
  (add-hook 'write-file-functions (lambda()
      (untabify (point-min) (point-max))
      nil))))

;;
;; http://www.emacswiki.org/emacs/AUCTeX
;;
(setq TeX-auto-save t)
    (setq TeX-parse-self t)
    (setq-default TeX-master nil)
    (add-hook 'LaTeX-mode-hook 'visual-line-mode)
    (add-hook 'LaTeX-mode-hook 'flyspell-mode)
    (add-hook 'LaTeX-mode-hook 'LaTeX-math-mode)
    (add-hook 'LaTeX-mode-hook 'turn-on-reftex)
    (setq reftex-plug-into-AUCTeX t)
(setq TeX-PDF-mode t)
(setq reftex-plug-into-AUCTeX t)

;(defun guess-TeX-master (filename)
;  "Guess the master file for FILENAME from currently open .tex files."
;  (let ((candidate nil)
;	(filename (file-name-nondirectory filename)))
;    (save-excursion
;      (dolist (buffer (buffer-list))
;	(with-current-buffer buffer
;	  (let ((name (buffer-name))
;		(file buffer-file-name))
;	    (if (and file (string-match "\\.tex$" file))
;		(progn
;		  (goto-char (point-min))
;		  (if (re-search-forward (concat "\\\\input{" filename "}") nil t)
;		      (setq candidate file))
;		  (if (re-search-forward (concat "\\\\include{" (file-name-sans-extension filename) "}") nil t)
;		      (setq candidate file))))))))
;    (if candidate
;	(message "TeX master document: %s" (file-name-nondirectory candidate)))
;    candidate))
;(setq TeX-master (guess-TeX-master (buffer-file-name)))
