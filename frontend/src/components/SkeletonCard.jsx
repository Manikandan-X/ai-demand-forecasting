export default function SkeletonCard() {

    return (

        <div
            className="
            bg-white
            p-5
            rounded-xl
            shadow
            animate-pulse
            "
        >

            <div
                className="
                h-4
                bg-gray-300
                rounded
                w-1/2
                mb-4
                "
            />

            <div
                className="
                h-8
                bg-gray-300
                rounded
                w-1/3
                "
            />

        </div>
    );
}