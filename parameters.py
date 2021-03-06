from utils import *
import os

class Parameters(object):
    def __init__(self, settings):
        #model parameters
        self.model_name             = settings["model_name"]        #a unique name for this configuration, change to something unique
        self.batch_size             = settings["batch_size"]
        self.num_classes            = settings["num_classes"]
        self.epochs                 = settings["epochs"]
        self.img_rows               = settings["img_rows"]
        self.img_cols               = settings["img_cols"]

        #path stuff
        self.root_dir_models        = settings["root_dir_models"]
        self.model_folder           = get_time_string()     #A model with be stored in a folder with just a date&time as folder name
        self.model_path             = os.path.join(self.root_dir_models, self.model_folder)     #path of model
        self.make_model_dir()       #create directory for all data concerning this model.
        
        #weights .h5 file
        self.weights_extension      = ".h5"                 #Extension for saving weights
        self.filename_weights       = self.model_name + "_weights_only" + self.weights_extension
        self.full_path_of_weights   = os.path.join(self.model_path, self.filename_weights)

        #csv logger file to store the callback of the .fit function. It stores the history of the training session.
        self.history_extension      = ".log"                 #Extension for history callback
        self.filename_history       = self.model_name + "_history" + self.history_extension
        self.full_path_of_history   = os.path.join(self.model_path, self.filename_history)

        #output path of .png
        self.figure_extension      = ".png"                 #Extension for figure 
        self.filename_figure       = self.model_name + "_results" + self.figure_extension
        self.full_path_of_figure   = os.path.join(self.model_path, self.filename_figure)


    def make_model_dir(self):
        try:
            os.mkdir(self.model_path)
        except OSError:
            print ("Creation of the directory %s failed" % self.model_path)
        else:
            print ("Successfully created the directory %s " % self.model_path)