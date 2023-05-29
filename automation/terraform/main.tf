data "ibm_resource_group" "group" {
  name = "Default"
}

resource "ibm_code_engine_project" "code_engine_project_instance" {
  name              = "my-project"
  resource_group_id = data.ibm_resource_group.group.id
}