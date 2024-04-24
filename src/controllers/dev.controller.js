const httpStatus = require('http-status');
const pick = require('../utils/pick');
const ApiError = require('../utils/ApiError');
const catchAsync = require('../utils/catchAsync');
const {devService} = require('../services'); 



const createDev = catchAsync (async (req,res) => {
  const dev = await devService.createDev(req.body);
    res.status(httpStatus.CREATED).send(dev);
});

const getDevs = catchAsync (async (req,res) => {
 const filter = pick(req.query, ['title']);
  const options = pick(req.query, ['sortBy', 'limit', 'page']);
  const { search } = pick(req.query, ['search']);
  const result = await devService.queryDevs(filter, options, search);
  res.send(result);
});


const getDev = catchAsync (async (req,res) => {
  console.log('get dev logs for test2dfs')
 const dev = await devService.getDevById(req.params.devId);
  if (!dev) {
    throw new ApiError(httpStatus.NOT_FOUND, 'Dev not found');
  }
  res.send(dev);
});



const updateDev = catchAsync (async (req,res) => {
    const dev = await devService.updateDevById(req.params.devId, req.body);
  res.send(dev);

});

const deleteDev = catchAsync (async (req,res) => {
  await devService.deleteDevById(req.params.devId);
  res.status(httpStatus.NO_CONTENT).send();
});

module.exports = {
  createDev,
  getDevs,
  getDev,
  updateDev,
  deleteDev,

};
