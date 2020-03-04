class Data:
  def __init__(self, parser_func, data_type, data_dir=None, data_file=None):
    self.data_dir = data_dir
    self.data_file = data_file
    self.data_type = data_type
    self.parser = parser_func

  def parse(self):
    if self.data_dir != None:
      import glob
      dir = self.data_dir+"*."+self.data_type
      files = glob.glob(dir)

      for file in files:
        yield self.parser(file)
    elif self.data_file != None:
      return self.parser(self.data_file)
    else:
      raise Exception("Please, pass a data to parse")

