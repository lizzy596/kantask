const httpStatus = require('http-status');
const { Dev } = require('../models');
const ApiError = require('../utils/ApiError');

const createDev = async (devBody) => {
return Dev.create(devBody);
};

const queryDevs = async (filter, options, search) => {
  const devs = await Dev.paginate(filter, options,search);
  return devs;
};


const getDevById = async (id) => {
  return Dev.findById(id);
};

const updateDevById = async (devId, updateBody) => {
  const dev = await getDevById(devId);
    if (!dev) {
    throw new ApiError(httpStatus.NOT_FOUND, 'Dev not found');
  }
  Object.assign(dev, updateBody);
  await dev.save();
  return dev;
};

const deleteDevById = async (devId) => {
    const dev = await getDevById(devId);
  if (!dev) {
    throw new ApiError(httpStatus.NOT_FOUND, 'Dev not found');
  }
  await dev.deleteOne();
  return dev;
};


module.exports = {
  createDev,
  queryDevs,
  getDevById,
  updateDevById,
  deleteDevById,
};
