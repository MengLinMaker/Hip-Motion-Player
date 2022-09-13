export default function csvToArray(str, delimiter = ",") {
  const rows = str.split('\n')
  const array = rows.map((row)=>{
    let rowArray = row.slice(0, str.indexOf("\r")).split(delimiter)
    rowArray = rowArray.map((number)=>{return parseFloat(number)})
    return rowArray
  })
  return array
}