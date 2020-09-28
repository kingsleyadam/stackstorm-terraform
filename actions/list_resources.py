import os
from lib import action


class ListResources(action.TerraformBaseAction):
	def run(self, plan_path, state_file_path, terraform_exec, target_address):
		"""
		List Terraform resources

		Args:
		- plan_path: path of the Terraform files
		- state_file_path: path of the Terraform state file
		- terraform_exec: path of the Terraform bin
		- target_address: filter list by address space

		Returns:
		- list: List of state resources
		"""
		self.terraform.terraform_bin_path = terraform_exec
		self.terraform.working_dir = os.path.expanduser(plan_path)
		self.terraform.state = state_file_path

		args = ['list', '-no-color']
		if target_address:
			args.append(target_address)

		return_code, stdout, stderr = self.terraform.state_cmd(*args)

		result = list()
		if stdout:
			result = stdout.rstrip().split('\n')

		if return_code == 0:
			return True, result
		else:
			return False, None

