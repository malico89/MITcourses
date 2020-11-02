# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import math

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # fits holds lists of coefficients
    fits = []
    
    # for each polynomial degree, run polyfit, and append to list of fits
    for degree in degs:
        coeff = pylab.polyfit(x, y, degree)
        # fits: list of pylab arrays
        fits.append(coeff)
    
    return fits

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # get mean of y values (original)
    mean_y = sum(y) / len(y)
    
    # # keep sum of numerator/denominator
    # total_num = 0
    # total_denom = 0
    # # loop over values in 1D arrays
    # for i in range(len(y)):x
    #     total_num += (y[i] - estimated[i])**2
    #     total_denom += (y[i] - mean_y)**2
        
    # using pylab array math
    total_num = sum((y - estimated)**2)
    total_denom = sum((y - mean_y)**2)
        
    # return R^2
    return 1 - (total_num/total_denom)

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # for each model, make a plot of x,y and that model
    for model in models:
        # get array of estimated values based on model
        est = pylab.polyval(model, x)
        # R^2 for current model     
        r_sq = r_squared(y, est)
            
        # title of plot includes degree of polynomial, R squared and SE/slope if linear
        title = 'Polynomial fit of degree {}\nR^2 = {:.5f}'.format(len(model)-1, r_sq)
        
        # if linear model, get SE over slope
        if len(model) == 2:
            SE_slope = se_over_slope(x, y, est, model)
            # append to title
            title += '\nSE over slope = {:.5f}'.format(SE_slope)
                    
        # generate plot for current model
        pylab.figure()
        pylab.plot(x, y, 'b.', label='Data')
        pylab.plot(x, est, 'r-', label='Fit')
        pylab.legend(loc='best')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (Celsius)')
        pylab.title(title)      
        

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # temps to hold annual average temp of all cities
    temps = []
    for year in years:
        # hold average temp for each city in a year
        city_temps = []
        for city in multi_cities:
            city_temps.append(pylab.mean(climate.get_yearly_temp(city, year)))
        # take average of all cities and add to temps
        temps.append(pylab.mean(pylab.array(city_temps)))
    return pylab.array(temps)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    mov_avg = []
    
    for i in range(len(y)):
        # for each item, store the sum of [i-window+1]->[i] in total, and keep
        # track of N items added in n (for start of array)
        total = 0
        n = 0
        for j in range(window_length):
            # only include if i-window index is >= 0
            if i-j >= 0:
                total += y[i-j]
                n += 1
        mov_avg.append(total/n)

    return pylab.array(mov_avg)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    sq_err = sum((y - estimated)**2)/len(y)
    return math.sqrt(sq_err)

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # same implementation as gen_cities_avg, but once we have all the 
    # temps_sd to hold annual standard deviation of temp of all cities over given years
    temps_sd = []
    for year in years:
        # hold temps for cities in this year
        city_temps = []
        for i in range(len(multi_cities)):
            # make a new sub-array to hold the daily temps of this city, this year
            city_temps.append([])
            # append 1D array of daily temps of that city
            city_temps[i].append(climate.get_yearly_temp(multi_cities[i], year))       
        # now collapse n*days array (n=number of cities) to 1D array where each element is
        # average daily temp across all cities (ave_city_temps)
        ave_city_temps = []         # len = n days in year
        # loop over days of the year
        for i in range(len(city_temps[0])):
            # day_temp holds sum of daily temp across cities
            day_temp = 0
            # loop over cities
            for j in range(len(multi_cities)):
                day_temp += city_temps[j][i]
            # store average day's temp
            ave_city_temps.append(day_temp/len(multi_cities))
        
        # take std across all days in the year
        temps_sd.append(pylab.std(pylab.array(ave_city_temps)))
    return pylab.array(temps_sd)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # similar implementation to evaluate_models_on_training
    # for each model, make a plot of x,y and that model
    for model in models:
        # get array of estimated values based on model
        est = pylab.polyval(model, x)
        # RMSE for current model     
        r_sq = rmse(y, est)
            
        # title of plot includes degree of polynomial, R squared and SE/slope if linear
        title = 'Polynomial fit of degree {}\nRMSE = {:.5f}'.format(len(model)-1, r_sq)
        
        # generate plot for current model
        pylab.figure()
        pylab.plot(x, y, 'b.', label='Data')
        pylab.plot(x, est, 'r-', label='Fit')
        pylab.legend(loc='best')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (Celsius)')
        pylab.title(title)

if __name__ == '__main__':

    # import data -- leave uncommented for creating Climate object
    data = Climate('data.csv')

    ################## Part A.4
    # 4.I: Sample January 10th, New York, from 1961 to 2009
    # 4.II: linear fit of average annual temperature
    # Generate x, y arrays for fitting and plotting (year, temps)
    # years = list(range(1961, 2010, 1))
    # x = pylab.array(years)
    # temps = []
    # temps_ave = []
    # for year in years:
    #     # 4.I: temp on a given day
    #     temps.append(data.get_daily_temp("NEW YORK", 1, 10, year))
    #     # 4.II: average temp on a given year
    #     temps_ave.append(pylab.mean(data.get_yearly_temp("NEW YORK", year)))
    # y  = pylab.array(temps)
    # y2 = pylab.array(temps_ave)
    # # fit to degree one polynomial
    # fit = generate_models(x, y, [1])
    # fit2 = generate_models(x, y2, [1]) 
    # # plot the regression result 
    # evaluate_models_on_training(x, y, fit)
    #evaluate_models_on_training(x, y2, fit2)
    # Observations on those two: taking Jan10 shows increase over time, but lower
    # intercept than taking the annual temp (winter month). Better linear fit
    # (per R^2) with annual average temp, but both fits are pretty bad. Fitting Jan10
    # also gives SE over slope > 0.5 (~0.6), which says fit is by chance (not
    # statistically significant). Data scatter looks more like noise than
    # using the average annual temp (taking the mean likely washes out some of
    # the noise). Positive slope for both validates temp increase over time.

    #################### Part B
    # Like Part A, but y values are now annual average over all cities
    # years = list(range(1961, 2010, 1))
    # x = pylab.array(years)
    # temps = []
    # y  = gen_cities_avg(data, CITIES, years)
    # # fit to degree one polynomial
    # fit = generate_models(x, y, [1])
    # # plot the regression result 
    # evaluate_models_on_training(x, y, fit)
    
    # When taking average over all cities, the fit gets even better (per R^2 and SE/slope). 
    # Again, I think averaging several times (over a day, over the year, over all cities)
    # washes out the noise (normalizes data around the mean). The upward trend
    # in temperatures is still evident. The fit would be noisier over less cities,
    # and tighter (less noisy) with more cities. Central limit theorem -- with larger
    # sample (aka more cities), the data point will more closely resemble the population mean.
    # With less cities, we may not even see the same trend, unless increase is inherent to
    # the data. If all cities were in the same region, I expect similar R^2 and
    # SE over slope, but the fit coefficients will likely change depending on region.

    ################### Part C
    # Same as part B, but use moving_average on the annual average temperatures
    # with window=5
    
    # list of years
    # years = list(range(1961, 2010, 1))
    # x = pylab.array(years)
    # temps = []
    # y = moving_average(gen_cities_avg(data, CITIES, years), 5)
    # # fit to degree one polynomial
    # fit = generate_models(x, y, [1])
    # # plot the regression result 
    # evaluate_models_on_training(x, y, fit)
    
    # This results in an even better fit per R^2 and SE/slope. The year to year swings get averaged out
    # so less noise in the data. What I'm learning: taking averages (over years
    # or samples) results in better fits -- but conceptually I would think multiple
    # averages might eventually "wash out" some signals. Averages are also
    # very susceptible to outliers, so a single outlier could amplify noise.
    # Either way, the fit is better, the trend shows siilar trend up over time.

    ######################### Part D.2
    # Train model using data from 1961-2009, and test it against data from 2010-2015
    # training data x,y
    # years = list(range(1961, 2010, 1))
    # x = pylab.array(years)
    # temps = []
    # y = moving_average(gen_cities_avg(data, CITIES, years), 5)
    # # fit to polynomials of degree 1, 2, 20
    # fits = generate_models(x, y, [1, 2, 20])
    # # plot the fits (training data, fits)
    # evaluate_models_on_training(x, y, fits)
    
    # As expected, R^2 increases for higher degree polynomials. By R^2 alone, 
    # degree 20 best fits the training data, but how good the model is depends on
    # test data

    # Generate test data - 5-year average temps from 2010-2015
    # years_test = list(range(2010, 2016, 1))
    # x_test = pylab.array(years_test)
    # y_test = moving_average(gen_cities_avg(data, CITIES, years_test), 5)
    
    # The best fit (based on RMSE of test data) is the linear fit. Quadratic
    # underestimates and degree 20 overestimates the tempratures for 2010-2016.
    # Linear model performed the best. These results are the opposite of what R^2
    # of the fits to the training data was telling us.
    
    # Test: fit models to average NYC temp 1961-2009 and then see how models perform
    # Prediction: worse fit
    # temps_ave = []
    # for year in years:
    #     # 4.II: average temp on a given year
    #     temps_ave.append(pylab.mean(data.get_yearly_temp("NEW YORK", year)))
    # y = pylab.array(temps_ave)
    # # fit to polynomials of degree 1, 2, 20
    # fits = generate_models(x, y, [1, 2, 20])
    # # plot the fits (training data, fits)
    # evaluate_models_on_training(x, y, fits)
    
    # # test models from part D using evalues_models_on_testing
    # evaluate_models_on_testing(x_test, y_test, fits)
    
    # Another observation: all models underpredict. Maybe NYC is on average a cooler 
    # city, so no model gets even close. Maybe if the testing data was of the same 
    # source (average annual NYC temp instead of 5-year rolling national average),
    # this set of models would perform better.
    
    #################### PART E
    # Extreme temperatures: gen_std_devs implemented to generate standard deviation
    # in a given year (daily tmeps are first averaged across all cities)
    years = list(range(1961, 2010, 1))
    # std dev 1D array
    sd_data = gen_std_devs(data, CITIES, years)
    # get 5-year moving averages of std dev
    sd_mov_avg = moving_average(sd_data, 5)
    # fit to degree 1 polynomial
    fit = generate_models(pylab.array(years), sd_mov_avg, [1])
    # plot results
    evaluate_models_on_training(pylab.array(years), sd_mov_avg, fit)
    
    # Trend and fit actually show a decreasing trend - meaning that over time,
    # the annual temp across is fluctuating less (even though the temps are going
    # up over time). To generate the std dev we first averaged daily temps across cities --
    # I think a good alternative would be to compute the std dev for a given city
    # over the course of the year, and then take the average of the std dev across
    # all cities. This would give the average annual fluctuation in a city,
    # and might tell us if fluctutations are getting worse over time.
    
    
    
