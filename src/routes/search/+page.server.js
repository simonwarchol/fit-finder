// export const ssr = false;
export const prerender = false;
export const ssr = false;
export async function load({url}) {
    const query = url.searchParams.get('query')
    return {query};
}