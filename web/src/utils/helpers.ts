export const truncate = (str:string, n=50) => str.length>n ? str.slice(0,n)+'...' : str;
