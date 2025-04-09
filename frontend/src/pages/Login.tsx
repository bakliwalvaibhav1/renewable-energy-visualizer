import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Navigate } from "react-router-dom";
import { api } from "../library/axios";
import { ToastContainer, toast } from "react-toastify";
import EcoViewLogo from "../assets/EcoView.png";

export default function Login() {
    const { isAuthenticated, login } = useAuth();
    const navigate = useNavigate();

    const [mode, setMode] = useState<"login" | "register">("login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);

    if (isAuthenticated) {
        return <Navigate to="/dashboard" />;
    }
    

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await api.post(
                "/auth/login",
                new URLSearchParams({ username: email, password }),
                {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                }
            );

            login(response.data.access_token);
            toast.success("Login successful!");
            navigate("/dashboard");
        } catch (err) {
            toast.error("Login failed. Please check your credentials.");
            console.error("Login error:", err);
        } finally {
            setLoading(false);
        }
    };


    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            toast.error("Passwords do not match!");
            return;
        }

        setLoading(true);

        try {
            await api.post("/auth/register", { email, password });
            toast.success("Registration successful! You can now log in.");
            setMode("login");
        } catch (err) {
            toast.error("Registration failed. Please try again.");
            console.error("Register error:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-200 to-green-400 via-white flex flex-col items-center justify-center p-6">
            {/* Logo */}
            <img src={EcoViewLogo} alt="EcoView" className="h-24 mb-6 mt-4" />

            {/* Card */}
            <div className="w-full max-w-md p-6 bg-white rounded shadow-md">
                {/* Tabs */}
                <div className="flex justify-center gap-4 mb-6">
                    <button
                        type="button"
                        className={`px-4 py-2 rounded ${
                            mode === "login"
                                ? "bg-green-500 text-white"
                                : "bg-gray-200"
                        }`}
                        onClick={() => setMode("login")}
                    >
                        Login
                    </button>
                    <button
                        type="button"
                        className={`px-4 py-2 rounded ${
                            mode === "register"
                                ? "bg-green-500 text-white"
                                : "bg-gray-200"
                        }`}
                        onClick={() => setMode("register")}
                    >
                        Register
                    </button>
                </div>

                {/* Form */}
                <form
                    onSubmit={mode === "login" ? handleLogin : handleRegister}
                    className="space-y-4"
                >
                    <input
                        type="email"
                        placeholder="Email"
                        className="w-full p-2 border rounded"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        className="w-full p-2 border rounded"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />

                    {mode === "register" && (
                        <input
                            type="password"
                            placeholder="Confirm Password"
                            className="w-full p-2 border rounded"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    )}

                    <button
                        type="submit"
                        className="w-full py-2 rounded text-white bg-green-500 hover:bg-green-600 flex justify-center items-center gap-2"
                        disabled={loading}
                    >
                        {loading && (
                            <svg
                                className="animate-spin h-5 w-5 text-white"
                                viewBox="0 0 24 24"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <circle
                                    className="opacity-25"
                                    cx="12"
                                    cy="12"
                                    r="10"
                                    stroke="currentColor"
                                    strokeWidth="4"
                                />
                                <path
                                    className="opacity-75"
                                    fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                                />
                            </svg>
                        )}
                        {mode === "login" ? "Login" : "Register"}
                    </button>
                </form>
            </div>

            <ToastContainer position="top-center" />
        </div>
    );
}
