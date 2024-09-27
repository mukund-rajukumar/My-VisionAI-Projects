def count_params(model):
  total_params = 0
  for param in model.parameters():
    num_elements = 1
    for dim in param.size():
       num_elements *= dim
    total_params += num_elements
  print(f"{total_params / 1000000:.1f} million parameters")