set shell := ["bash", "-cu"]

update input:
	@rm next-step.md
	@echo "{{input}}" >> next-step.md

	cat next-step.md
