# Optimize your PID parameters here:
pressure_tau_p = 0.1
pressure_tau_d = 0.7

rocket_tau_p = 11
rocket_tau_i = 0.01
rocket_tau_d = 3


def pressure_pd_solution(delta_t, current_pressure, data):
    """Student solution to maintain LOX pressure to the turbopump at a level of 100.

    Args:
        delta_t (float): Time step length.
        current_pressure (float): Current pressure level of the turbopump.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0
    """

    # TODO: remove naive solution
    #adjust_pressure = current_pressure

    # TODO: implement PD solution here
    prev_P_error=data['ErrorP']
    P_error=current_pressure-100
    D_error=(P_error-prev_P_error)/delta_t
    adjust_pressure=-pressure_tau_p * P_error - pressure_tau_d * D_error
    data['ErrorP'] = P_error
    data['ErrorD'] = D_error

    return adjust_pressure, data


def rocket_pid_solution(delta_t, current_velocity, optimal_velocity, data):
    """Student solution for maintaining rocket throttle through out the launch based on an optimal flight path

    Args:
        delta_t (float): Time step length.
        current_velocity (float): Current velocity of rocket.
        optimal_velocity (float): Optimal velocity of rocket.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorI': Integral error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0

    Returns:
        Throttle to set, data dictionary to be passed through run.
    """

    # TODO: remove naive solution
    #throttle = optimal_velocity - current_velocity

    # TODO: implement PID Solution here
    prev_P_error = data['ErrorP']
    prev_I_error=data['ErrorI']
    P_error = optimal_velocity-current_velocity
    D_error = (P_error - prev_P_error) / delta_t
    I_error=prev_I_error+P_error*delta_t
    if optimal_velocity>=0.3: # adding offset to the throttle equation as per dicussion on Piazza, also using different offset values on different steps
        throttle = rocket_tau_p * P_error + rocket_tau_d * D_error + rocket_tau_i * I_error+0.44
    elif optimal_velocity>=0:
        throttle = rocket_tau_p * P_error + rocket_tau_d * D_error + rocket_tau_i * I_error+0.25
    else:
        throttle = rocket_tau_p * P_error + rocket_tau_d * D_error+rocket_tau_i*I_error+0.7
    data['ErrorP'] = P_error
    data['ErrorD'] = D_error
    data['ErrorI'] = I_error


    return throttle, data