export const getEnv = (variable: string | undefined, name: string) => {
    if (!variable) {
        throw new Error(`${name} is not founded`)
    }

    return variable
}