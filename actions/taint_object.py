import os
from lib import action
from python_terraform import IsFlagged, IsNotFlagged


class Taint(action.TerraformBaseAction):
	def run(self, plan_path, state_file_path, target_resources, terraform_exec, allow_missing):
		"""
		Taint a list of resources

		Args:
		- plan_path: path of the Terraform files
		- state_file_path: path of the Terraform state file
		- target_resources: list of resources to target from the configuration
		- terraform_exec: path of the Terraform bin
		- allow_missing: If specified, the command will succeed (exit code 0) even if the resource is missing.

		Returns:
		- dict: Terraform taint command output
		"""
		self.terraform.terraform_bin_path = terraform_exec
		self.terraform.working_dir = os.path.expanduser(plan_path)

		return_code = 0
		stdout = ''
		stderr = ''
		for resource in target_resources:
			_cmd_return_code, _cmd_stdout, _cmd_stderr = self.terraform.taint_cmd(
				resource,
				state=state_file_path,
				allow_missing=IsFlagged if allow_missing else IsNotFlagged,
				capture_output=False,
				no_color=IsFlagged
			)
			if isinstance(_cmd_stdout, str):
				stdout += _cmd_stdout
			if isinstance(_cmd_stderr, str):
				stderr += _cmd_stderr

			# If any taint command returns != 0, make sure the whole method returns != 0.
			if _cmd_return_code != 0:
				return_code = _cmd_return_code

		return self.check_result(return_code, stdout, stderr, return_output=False)
