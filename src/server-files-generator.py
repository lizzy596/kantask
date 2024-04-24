# 1. Bring in variables (example: 'profile')
# 2. Create service
# 3. Create controller (wtih path to service in imports)
# 4. Create route with path to controller

# NOTE: Run from root directory

# python server-files-generator.py 'profile'

import sys
import os

# Create service
print("Creating Files...")

def create_file(directory, filename, type):
    with open(directory + '/' + filename + '.' + type  + '.js', "w") as f:
        f.write("")

def append_file(path, text):
    with open(path, "a") as f:
        f.write(text)
        f.close()

def wordCheck(count):
      word_array = []  
      while len(word_array) < count:
        user_input = input("Enter a word: ")
        word_array.append(user_input)

      print("Generating:")
      camel_array = [word_array[0]] + [word.capitalize() for word in word_array[1:]]
      capitalized_array = [word.capitalize() for word in word_array]
      camel_fileName = ''.join(camel_array)
      model_fileName = ''.join(capitalized_array)
      return camel_fileName, model_fileName


wordCount = 0
user_input=""
filename = ""
#word_array = []



if __name__ == "__main__":
  wordCount = int(input("Enter the number of discrete words contained in your fileName: "))
  c, m = wordCheck(wordCount)


  #user_input = input("Enter word: ")
  #my_array.append(user_input)
  # filename = input("Enter the name of the file to create: ")
  # modelname = filename.capitalize()

#Create model

create_file('models', c, 'model')

valExport = "\nmodule.exports.%s = require('./%s.model');" % (m, c)
append_file('models/index.js', valExport)
append_file('models/%s.model.js' % (c), 
"""const mongoose = require('mongoose');
const { toJSON, paginate } = require('./plugins');

const %sSchema = mongoose.Schema(
  {
    question: {
      type: String,
      required: true,
    },
    explanation: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

// add plugin that converts mongoose to json
%sSchema.plugin(toJSON);
%sSchema.plugin(paginate);



%sSchema.statics.searchableFields = function () {
  return ['category'];
};

const %s = mongoose.model('%s', %sSchema);

module.exports = %s;


""" % (c,c,c,c,m,m,c,m))

# # Create Service
create_file('services', c, 'service')

serviceExport = "\nmodule.exports.%sService = require('./%s.service');" % (c, c)
append_file('services/index.js', serviceExport)
append_file('services/%s.service.js' % (c), 
"""const httpStatus = require('http-status');
const { %s } = require('../models');
const ApiError = require('../utils/ApiError');

const create%s = async (%sBody) => {
return %s.create(%sBody);
};

const query%ss = async (filter, options, search) => {
  const %ss = await %s.paginate(filter, options,search);
  return %ss;
};


const get%sById = async (id) => {
  return %s.findById(id);
};

const update%sById = async (%sId, updateBody) => {
  const %s = await get%sById(%sId);
    if (!%s) {
    throw new ApiError(httpStatus.NOT_FOUND, '%s not found');
  }
  Object.assign(%s, updateBody);
  await %s.save();
  return %s;
};

const delete%sById = async (%sId) => {
    const %s = await get%sById(%sId);
  if (!%s) {
    throw new ApiError(httpStatus.NOT_FOUND, '%s not found');
  }
  await %s.deleteOne();
  return %s;
};


module.exports = {
  create%s,
  query%ss,
  get%sById,
  update%sById,
  delete%sById,
};
""" % (m,m,c,m,c,m,c,m,c,m,m,m,c,c,m,c,c,m,c,c,c,m,c,c,m,c,c,m,c,c,m,m,m,m,m ))

# Controllers
create_file('controllers', c, 'controller')

controllerExport = "\nmodule.exports.%sController = require('./%s.controller');" % (c, c)
append_file('controllers/index.js', controllerExport)
append_file('controllers/%s.controller.js' % (c),
"""const httpStatus = require('http-status');
const pick = require('../utils/pick');
const ApiError = require('../utils/ApiError');
const catchAsync = require('../utils/catchAsync');
const {%sService} = require('../services'); 



const create%s = catchAsync (async (req,res) => {
  const %s = await %sService.create%s(req.body);
    res.status(httpStatus.CREATED).send(%s);
});

const get%ss = catchAsync (async (req,res) => {
 const filter = pick(req.query, ['title']);
  const options = pick(req.query, ['sortBy', 'limit', 'page']);
  const { search } = pick(req.query, ['search']);
  const result = await %sService.query%ss(filter, options, search);
  res.send(result);
});


const get%s = catchAsync (async (req,res) => {
 const %s = await %sService.get%sById(req.params.%sId);
  if (!%s) {
    throw new ApiError(httpStatus.NOT_FOUND, '%s not found');
  }
  res.send(%s);
});

const update%s = catchAsync (async (req,res) => {
    const %s = await %sService.update%sById(req.params.%sId, req.body);
  res.send(%s);

});

const delete%s = catchAsync (async (req,res) => {
  await %sService.delete%sById(req.params.%sId);
  res.status(httpStatus.NO_CONTENT).send();
});

module.exports = {
  create%s,
  get%ss,
  get%s,
  update%s,
  delete%s,

};
""" % (c,m,c,c,m,c,m,c,m,m,c,c,m,c,c,m,c,m,c,c,m,c,c,m,c,m,c,m,m,m,m,m))

# # Routes
create_file('routes/v1', c, 'route');
routeExport = "\nconst %sRoute = require('./%s.route');" % (c, c)

with open('routes/v1/index.js') as f:
    read_data = f.read()
with open('routes/v1/index.js', 'w') as f:
    f.write(routeExport + read_data)




# #append_file('routes/v1/index.ts', routeExport)
append_file('routes/v1/%s.route.js' % (c), 
"""const express = require('express');
const auth = require('../../middlewares/auth');
const validate = require('../../middlewares/validate');
const %sValidation = require('../../validations/%s.validation');
const %sController = require('../../controllers/%s.controller');

const router = express.Router();



router
  .route('/')
  .post(validate(%sValidation.create%s), %sController.create%s)
  .get(auth(''), validate(%sValidation.get%s), %sController.get%ss);


router
  .route('/:%sId')
  .get(auth(''), validate(%sValidation.get%s), %sController.get%s)
  .patch(auth(''), validate(%sValidation.update%s), %sController.update%s)
  .delete(auth(''), validate(%sValidation.delete%s), %sController.delete%s);

module.exports = router;
""" % (c,c,c,c,c,m,c,m,c,m,c,m,c,c,m,c,m,c,m,c,m,c,m,c,m))

# # Validations
create_file('validations', c, 'validation')

valExport = "\nmodule.exports.%sValidation = require('./%s.validation')" % (c,c)
append_file('validations/index.js', valExport)
append_file('validations/%s.validation.js' % (c), 
"""const Joi = require('joi');
const { objectId } = require('./custom.validation');

const create%s = {
  body: Joi.object().keys({
    email: Joi.string().required()
  }),
};

const get%ss = {
  query: Joi.object().keys({
    firstName: Joi.string(),
    lastName: Joi.string(),
    role: Joi.string(),
    search: Joi.string().allow(''),
    sortBy: Joi.string(),
    limit: Joi.number().integer(),
    page: Joi.number().integer(),
  }),
};

const get%s = {
  params: Joi.object().keys({
    %sId: Joi.string().custom(objectId),
  }),
};

const update%s = {
  params: Joi.object().keys({
    %sId: Joi.required().custom(objectId),
  }),
  body: Joi.object()
    .keys({
      firstName: Joi.string(),
      lastName: Joi.string(),
    })
    .min(1),
};


const delete%s = {
  params: Joi.object().keys({
    %sId: Joi.string().custom(objectId),
  }),
};

module.exports = {
  create%s,
  get%ss,
  get%s,
  update%s,
  delete%s,
};
""" % (m,m,m,c,m,c,m,c,m,m,m,m,m))