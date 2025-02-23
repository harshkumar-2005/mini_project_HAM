export const validateEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
  };
  
  export const validatePassword = (password) => {
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
    return passwordRegex.test(password);
  };
  
  export const validateRequired = (value) => {
    return value?.trim().length > 0;
  };
  
  export const validateField = (field, value) => {
    const validators = {
      email: validateEmail,
      password: validatePassword,
      required: validateRequired,
    };
    
    return validators[field] ? validators[field](value) : true;
  };
  